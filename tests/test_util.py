import unittest
from module.util import Util

class TestExtension(unittest.TestCase):

    def test_is_file(self):
        test_file = 'test.txt'
        self.assertTrue(Util.is_file(test_file))

    def test_is_not_file(self):
        test_dir = 'folderA'
        self.assertFalse(Util.is_file(test_dir))

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

    def test_generate_path_to_dest_file(self):
        raw_filename = "Movie episode \/'1.mkv"
        valid_sanitized_filename = "Movie episode 1.mkv"
        dest_path = 'dest/'
        valid_sanitized_path_to_dest_file = dest_path + valid_sanitized_filename

        sanitized_path_to_dest_file = Util.generate_path_to_dest_file(dest_path, raw_filename)

        self.assertEqual(sanitized_path_to_dest_file, valid_sanitized_path_to_dest_file)

    def test_generate_path_to_src_file(self):
        valid_filename = "Movie episode 1.mkv"
        src_path = 'src/'
        valid_sanitized_path_to_src_file = src_path + valid_filename

        path_to_src_file = Util.generate_path_to_src_file(src_path, valid_filename)

        self.assertEqual(path_to_src_file, valid_sanitized_path_to_src_file)

    def test_sanitize_filename_for_rclone(self):
        valid_filename = "Movie episode 1.mkv"
        raw_filename = "Movie episode '1.mkv"

        sanitized_filename = Util.sanitize_filename_for_rclone(raw_filename)

        self.assertEqual(sanitized_filename, valid_filename)