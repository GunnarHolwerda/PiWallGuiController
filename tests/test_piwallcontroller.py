__author__ = 'Gunnar'

import unittest
from os.path import dirname, abspath
from piwallcontroller import *

BASE_PATH = dirname(dirname(abspath(__file__))) + "/"
VIDEO_PATH = BASE_PATH + "videos/"

class TestPlaylist(unittest.TestCase):

    def setUp(self):
        self.playlist = Playlist()

    def tearDown(self):
        self.playlist = None

    def test_add_playlist_item(self):
        self.playlist.add_playlist_item('test', 1)
        self.assertEqual(len(self.playlist.get_items()), 1)

    def test_remove_playlist_item(self):
        self.playlist.add_playlist_item('test', 1)
        self.playlist.add_playlist_item('test', 2)
        self.playlist.add_playlist_item('test', 3)
        self.playlist.remove_playlist_item([2])
        self.assertEqual(len(self.playlist.get_items()), 2)

    def test_remove_playlist_item_removes_correct_item(self):
        self.playlist.add_playlist_item('test1', 1)
        self.playlist.add_playlist_item('test2', 2)
        self.playlist.add_playlist_item('test3', 3)
        self.playlist.remove_playlist_item([1])
        self.assertEqual(self.playlist.get_items()[1].get_video_file(), VIDEO_PATH + 'test3')

    def test_is_empty(self):
        self.assertEqual(self.playlist.is_empty(), True)


class TestPiWallController(unittest.TestCase):
    def setUp(self):
        self.playlist = Playlist()
        self.playlist.add_playlist_item('test1', 1)
        self.playlist.add_playlist_item('test2', 2)

    def tearDown(self):
        self.playlist = None


if __name__ == '__main__':
    unittest.main()
