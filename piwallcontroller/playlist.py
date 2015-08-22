from os.path import dirname, abspath

BASE_PATH = dirname(dirname(abspath(__file__))) + "/"
VIDEO_PATH = BASE_PATH + "videos/"


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
