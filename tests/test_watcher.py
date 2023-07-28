import unittest
from module.watcher import Watcher
from module.record import Record
import os

class TestWatcher(unittest.TestCase):

    def setUp(self):
        allowed_exts = ['.jpg', '.mkv', '.avi']
        self.record = Record('test.db')
        self.record.open()
        self.record.close()
        self.watcher = Watcher('', '', allowed_exts, self.record)

    def tearDown(self):
        os.remove('test.db')

    def test_valid_exts_match_filename_match_allowed_exts(self):
        filename_valid_exts = "episode 3.mkv"

        self.assertTrue(self.watcher.filename_match_allowed_exts(filename_valid_exts))

    def test_missing_exts_filename_match_allowed_exts(self):
        filename_missing_exts = "episode 4"

        self.assertFalse(self.watcher.filename_match_allowed_exts(filename_missing_exts))

    def test_valid_exts_not_match_filename_match_allowed_exts(self):
        filename_valid_exts_but_not_match = "episode 4.docx"

        self.assertFalse(self.watcher.filename_match_allowed_exts(filename_valid_exts_but_not_match))

    def test_valid_new_file_is_new_file_obj(self):
        valid_new_filename = "episode 4.mkv"

        self.assertTrue(self.watcher.is_new_file_obj(valid_new_filename))

    def test_valid_old_file_is_new_file_obj(self):
        valid_old_filename = "episode 4.mkv"

        self.record.open()
        self.record.store(valid_old_filename)
        self.record.close()

        self.assertFalse(self.watcher.is_new_file_obj(valid_old_filename))