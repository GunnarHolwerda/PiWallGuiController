"""
    Represents a command for the pi
"""

class Command:
    """
        Represents a Command to be run on the pi including a timeout
    """
    BASE_COMMAND_STR = "avconv -re -i {0} -vcodec copy -f avi -an udp://239.0.1.23:1234"

    def __init__(self, video_file, timeout=0):
        self.__timeout = timeout
        self.__video_file = video_file
        self.__command_str = self.BASE_COMMAND_STR.format(video_file)

    def get_timeout(self):
        """
            Returns the timeout for the command
            :return int: timeout
        """
        return int(self.__timeout)

    def get_video_file(self):
        """
            Returns video file that is playing in this command
        """
        return self.__video_file

    def get_command_str(self):
        """
            Returns the command string for the command

            :return str, cmd string
        """
        return self.__command_str

    def __str__(self):
        return self.__command_str
