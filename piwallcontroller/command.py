"""
    Represents a command for the pi
"""

class Command:
    """
        Represents a Command to be run on the pi including a timeout
    """

    def __init__(self, command_str, timeout=0):
        self.__timeout = timeout
        self.__command_str = command_str

    def get_timeout(self):
        """
            Returns the timeout for the command
            :return int: timeout
        """
        return int(self.__timeout)

    def get_command_str(self):
        """
            Returns the command string for the command

            :return str, cmd string
        """
        return self.__command_str

    def __str__(self):
        return self.__command_str
