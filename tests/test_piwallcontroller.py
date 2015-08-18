__author__ = 'Gunnar'

import unittest
from piwallcontroller.piwallcontroller import *


class TestPlaylist(unittest.TestCase):

    def setUp(self):
        self.playlist = Playlist()

    def tearDown(self):
        self.playlist = None

    def test_add_playlist_item(self):
        self.playlist.add_playlist_item('test', 1)
        self.assertEqual(len(self.playlist.get_playlist()), 1)

    def test_remove_playlist_item(self):
        self.playlist.add_playlist_item('test', 1)
        self.playlist.add_playlist_item('test', 2)
        self.playlist.add_playlist_item('test', 3)
        self.playlist.remove_playlist_item([2])
        self.assertEqual(len(self.playlist.get_playlist()), 2)

    def test_remove_playlist_item_removes_correct_item(self):
        self.playlist.add_playlist_item('test1', 1)
        self.playlist.add_playlist_item('test2', 2)
        self.playlist.add_playlist_item('test3', 3)
        self.playlist.remove_playlist_item([1])
        self.assertEqual(self.playlist.get_playlist()[1].get_video_file(), VIDEO_PATH + 'test3')

    def test_is_empty(self):
        self.assertEqual(self.playlist.is_empty(), True)


class TestPiWallController(unittest.TestCase):
    def setUp(self):
        self.playlist = Playlist()
        self.playlist.add_playlist_item('test1', 1)
        self.playlist.add_playlist_item('test2', 2)

    def tearDown(self):
        self.playlist = None

    def test_build_commands(self):
        controller = PiWallController()
        assertion_strings = []
        for i in range(0, 2):
            assertion_strings.append(controller.BASE_COMMAND_STR.format(self.playlist.get_playlist()[i]))
        commands = controller.build_commands(self.playlist)
        i = 0
        for command in commands:
            self.assertEqual(command.get_command_str(), assertion_strings[i])
            i += 1


if __name__ == '__main__':
    unittest.main()