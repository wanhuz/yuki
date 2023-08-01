import unittest
from module.util import Util

class TestUtil(unittest.TestCase):

    def test_valid_is_file(self):
        test_file = 'test.txt'
        self.assertTrue(Util.is_file(test_file))

    def test_valid_is_not_file(self):
        test_dir = 'folderA'
        self.assertFalse(Util.is_file(test_dir))

    def test_valid_get_extension_filename(self):
        valid_filename = "photo.jpg"
        self.assertEqual(Util.get_extension(valid_filename), ".jpg")

    def test_invalid_get_extension_filename(self):
        invalid_filename = "photo"
        self.assertFalse(Util.get_extension(invalid_filename))

    def test_numbered_get_extension_filename(self):
        valid_filename = "23123123.png"
        self.assertEqual(Util.get_extension(valid_filename), ".png")

    def test_japanese_get_extension_filename(self):
        japanese_filename = "わたしわ.mkv"
        self.assertEqual(Util.get_extension(japanese_filename), ".mkv")

    def test_generate_path_to_dest_file(self):
        dest_path = 'dest/'
        filename = "Movie episode 1.mkv"
        valid_filename = "Movie episode 1.mkv"
        valid_sanitized_path_to_dest_file = dest_path + valid_filename

        sanitized_path_to_dest_file = Util.generate_path_to_dest_file(dest_path, filename)

        self.assertEqual(sanitized_path_to_dest_file, valid_sanitized_path_to_dest_file)

    def test_generate_path_to_src_file(self):
        src_path = 'src/'
        valid_filename = "Movie episode 1.mkv"
        valid_sanitized_path_to_src_file = src_path + valid_filename

        path_to_src_file = Util.generate_path_to_src_file(src_path, valid_filename)

        self.assertEqual(path_to_src_file, valid_sanitized_path_to_src_file)

    def test_escape_quotes_parser_single_quote(self):
        valid_filename = r"Episode '\''4"
        raw_filename = "Episode '4"

        sanitized_filename = Util.escape_quotes_parser(raw_filename)

        self.assertEqual(sanitized_filename, valid_filename)

    def test_escape_quotes_parser_double_quote(self):
        valid_filename = r'Episode "\""4'
        raw_filename = 'Episode "4'

        sanitized_filename = Util.escape_quotes_parser(raw_filename)

        self.assertEqual(sanitized_filename, valid_filename)

    def test_escape_quotes_parser_no_quote(self):
        valid_filename = 'Episode 4'
        raw_filename = 'Episode 4'

        sanitized_filename = Util.escape_quotes_parser(raw_filename)

        self.assertEqual(sanitized_filename, valid_filename)