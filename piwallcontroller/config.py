"""
    File holding PiWall Config class
"""

from os.path import dirname, abspath

BASE_PATH = dirname(dirname(abspath(__file__))) + "/"
VIDEO_PATH = BASE_PATH + "videos/"


class Config:
    """
        Class to represent all configs for the current PiWall
    """
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
