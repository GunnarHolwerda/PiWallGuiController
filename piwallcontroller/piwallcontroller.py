"""
    File holding the class to control the PiWall
"""
# Author Gunnar Holwerda
# Creation date: 8/11/2015
# Last edit: 8/12/2015

from piwallcontroller.command import Command
from piwallcontroller.config import Config
from subprocess import call
from os.path import dirname, abspath
import time

BASE_PATH = dirname(dirname(abspath(__file__))) + "/"
VIDEO_PATH = BASE_PATH + "videos/"


class PiWallController:
    """
        Class that controls the PiWall
    """
    NUMBER_OF_TILES = Config.get_num_of_tiles()

    def __init__(self):
        self.__video_files = Config.load_video_files()
        self.__tiles = Config.load_tiles()
        self.__tiles_on = False
        self.__stop_flag = True
        self.__current_video = ""

    def run_commands(self, playlist):
        """
            Runs all necessary commands to start the tiles and then starts the master
        """
        if not self.__tiles_on:
            self.turn_on_tiles()

        for item in playlist.get_items():
            end_time = int(time.time()) + item.get_timeout()
            while (int(time.time()) < end_time and self.__stop_flag is True) \
                or item.get_timeout == -1:
                call(item.get_command(), shell=True)

        playlist.clear_playlist()

        self.__stop_flag = True

    def stop_wall(self):
        """
            Stops the wall from running
        """
        self.__stop_flag = False

    def turn_on_tiles(self):
        """
            Starts all tiles
        """
        remote_command = "pwomxplayer --config={0} udp://239.0.1.23:1234?buffer_size=1200000B" \
            .format(Config.get_config_name())
        for tile in self.__tiles:
            call("nohup sshpass -p raspberry ssh {0} '{1}' > /dev/null 2>&1 &".format(
                tile['ip'],
                remote_command), shell=True)
            time.sleep(1)
        self.__tiles_on = True

    def reboot_pis(self):
        """
            Reboots all tiles
        """
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

    def get_current_playing_video(self):
        """
            Returns the current playing video
        """
        return self.get_current_playing_video
