import unittest
from module.util import Util

class TestExtension(unittest.TestCase):

    def test_valid_filename(self):
        valid_filename = "photo.jpg"
        self.assertEqual(Util.get_extension(valid_filename), ".jpg")

    def test_invalid_filename(self):
        invalid_filename = "photo"
        self.assertFalse(Util.get_extension(invalid_filename))

    def test_numbered_filename(self):
        valid_filename = "23123123.png"
        self.assertEqual(Util.get_extension(valid_filename), ".png")

    def test_japanese_filename(self):
        japanese_filename = "わたしわ.mkv"
        self.assertEqual(Util.get_extension(japanese_filename), ".mkv")