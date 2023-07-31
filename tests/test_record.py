import unittest
import os
from module.record import Record
import random

class TestRecord(unittest.TestCase):

    def setUp(self):
        self.record = Record('test.db')
        self.record.open()

    def tearDown(self):
        self.record.close()
        os.remove('test.db')

    def test_is_match(self):
        valid_matching_filename = "Episode " + str(random.randint(1, 9))

        self.record.store(valid_matching_filename)
        
        self.assertTrue(self.record.is_match(valid_matching_filename))

    def test_is_not_match(self):
        valid_matching_filename = "Episode " + str(random.randint(1, 9))
        invalid_matching_filenname = "Episode 100"

        self.record.store(valid_matching_filename)
        
        self.assertFalse(self.record.is_match(invalid_matching_filenname))

    def test_delete_contains(self):
        valid_filename_suffix = "Episode "
        valid_filename = "Episode " + str(random.randint(1, 9))

        for i in range(1, 10):
            self.record.store(valid_filename_suffix + str(i))

        self.record.delete_contains(valid_filename_suffix)

        self.assertFalse(self.record.search_contains(valid_filename))

    def test_valid_search_contains(self):
        valid_filename_contains = "Episode 2"
        store_filenames = ['Episode 23', 'Episode 24']

        for filename in store_filenames:
            self.record.store(filename)

        search_result = self.record.search_contains(valid_filename_contains)
        search_result_count = len(search_result)

        self.assertEqual(search_result_count, 2)

    def test_invalid_search_contains(self):
        invalid_filename_contains = "Episode 1"
        store_filenames = ['Episode 23', 'Episode 24']

        for filename in store_filenames:
            self.record.store(filename)

        search_result = self.record.search_contains(invalid_filename_contains)
        search_result_count = len(search_result)

        self.assertEqual(search_result_count, 0)