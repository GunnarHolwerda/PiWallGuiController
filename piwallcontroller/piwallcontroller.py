# Author Gunnar Holwerda
# Creation date: 8/11/2015
# Last edit: 8/12/2015

from subprocess import call
import time
from os.path import dirname, abspath

BASE_PATH = dirname(dirname(abspath(__file__))) + "/"
VIDEO_PATH = BASE_PATH + "videos/"


class PlaylistItem:
    def __init__(self, video_file, timeout):
        self.__video_file = video_file
        self.__timeout = timeout

    def get_timeout(self):
        """
            Returns the timeout for the playlist item
            :rtype : int
            :return the length of the timeout in seconds
            """
        return self.__timeout

    def get_video_file(self):
        """
            Returns the video file name for the playlist item
            :rtype : str
            :return the string for the video file
            """
        return VIDEO_PATH + self.__video_file

    def __str__(self):
        return self.get_video_file()


class Playlist:
    def __init__(self):
        self.__playlist = []

    def add_playlist_item(self, video_file, timeout):
        self.__playlist.append(PlaylistItem(video_file, timeout))

    def get_playlist(self):
        """
        Returns the list of PlaylistItems in the playlist
        :rtype : list[PlaylistItem]
        :return list of playlist items in the playlist
        """
        return self.__playlist

    def remove_playlist_item(self, index):
        del self.__playlist[index[0]]

    def is_empty(self):
        """
        Returns if the list is empty or not
        :rtype : bool
        :return true if playlist is empty, false otherwise
        """
        return not self.__playlist

    def clear_playlist(self):
        del self.__playlist[:]

    def __str__(self):
        return str(len(self.__playlist))


class Command:
    def __init__(self, command_str, timeout=0):
        self.__timeout = timeout
        self.__command_str = command_str

    def get_timeout(self):
        return int(self.__timeout)

    def get_command_str(self):
        return self.__command_str

    def __str__(self):
        return self.__command_str


class Config:
    @staticmethod
    def load_tiles():
        """
        Returns the tiles for the Pi Wall
        :rtype : list
        :return: list of tiles
        """
        from piwallcontroller import wall
        return wall.configs['tiles']

    @staticmethod
    def load_video_files():
        """
        Returns a list of videos in the videos directory
        :rtype : list
        :return: returns list of videos in the videos directory
        """
        from os import listdir
        return listdir(VIDEO_PATH)

    @staticmethod
    def load_master_ip():
        """
        Returns the ip of the master pi (this pi)
        :rtype : str
        :return: returns the ip address of the pi
        """
        from piwallcontroller import wall
        return wall.master_ip

    @staticmethod
    def get_num_of_tiles():
        """
        Returns the number of tiles in the walls from wall.py
        :rtype : int
        :return: the number of tiles in the wall
        """
        from piwallcontroller import wall
        return wall.configs['num_of_tiles']

    @staticmethod
    def get_config_name():
        """
        Returns the first config name in wall.py
        :rtype : str
        :return: the first config name in the config file
        """
        from piwallcontroller import wall
        return wall.configs['config'][0]['name']


class PiWallController:
    NUMBER_OF_TILES = Config.get_num_of_tiles()
    BASE_COMMAND_STR = "avconv -re -i {0} -vcodec copy -f avi -an udp://239.0.1.23:1234"

    def __init__(self):
        self.__video_files = Config.load_video_files()
        self.__tiles = Config.load_tiles()
        self.__tiles_on = False
        self.__stop_flag = True

    def build_commands(self, playlist):
        """
        Builds up the list of commands to run for the current PiWall setup
        :rtype : list
        :return: list of commands to be run
        """
        commands = []
        for playlist_item in playlist.get_playlist():
            commands.append(Command(self.BASE_COMMAND_STR.format(playlist_item.get_video_file()),
                                    playlist_item.get_timeout()))

        playlist.clear_playlist()

        return commands

    def run_commands(self, playlist):
        if not self.__tiles_on:
            self.turn_on_tiles()
        commands = self.build_commands(playlist)
        for command in commands:
            end_time = int(time.time()) + command.get_timeout()
            while int(time.time()) < end_time and self.__stop_flag is True:
                call(command.get_command_str(), shell=True)
        self.__stop_flag = True

    def stop_wall(self):
        self.__stop_flag = False

    def turn_on_tiles(self):
        remote_command = "pwomxplayer --config={0} udp://239.0.1.23:1234?buffer_size=1200000B" \
            .format(Config.get_config_name())
        for tile in self.__tiles:
            call("nohup sshpass -p raspberry ssh {0} '{1}' > /dev/null 2>&1 &".format(tile['ip'], remote_command),
                 shell=True)
            time.sleep(1)
        self.__tiles_on = True

    def reboot_pis(self):
        self.__tiles_on = False
        self.stop_wall()
        reboot_command = "nohup sshpass -p raspberry ssh {0} 'sudo reboot' > /dev/null 2>&1 &"
        for tile in self.__tiles:
            print("Rebooting tile with ip {0}".format(tile['ip']))
            call(reboot_command.format(tile['ip']), shell=True)
        self.__stop_flag = True

    def get_video_file_list(self):
        """
        Returns a list of the video files in the video/ directory
        :rtype  : list
        :return: list of the video files in the videos/ directory
        """
        return self.__video_files
