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
