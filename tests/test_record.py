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

    def test_valid_search_store(self):
        valid_filename_suffix = "Episode "
        valid_search_filename = "Episode " + str(random.randint(1, 9))

        for i in range(1, 10):
            self.record.store(valid_filename_suffix + str(i))

        search_result = self.record.search(valid_search_filename)

        for search in search_result:
            self.assertEqual(search['name'], valid_search_filename)

    def test_invalid_search(self):
        valid_filename_suffix = "Episode "
        invalid_search_filename = "Episode 100"

        for i in range(1, 10):
            self.record.store(valid_filename_suffix + str(i))

        search_result = self.record.search(invalid_search_filename)

        for search in search_result:
            self.assertFalse(search['name'], invalid_search_filename)

    def test_delete_all(self):
        valid_filename = "Episode 4"

        for i in range(1, 10):
            self.record.store(valid_filename)

        self.record.delete_all(valid_filename)

        self.assertFalse(self.record.search(valid_filename))

    def test_is_match(self):
        valid_matching_filename = "Episode " + str(random.randint(1, 9))

        self.record.store(valid_matching_filename)
        
        self.assertTrue(self.record.is_match(valid_matching_filename))

    def test_is_not_match(self):
        valid_matching_filename = "Episode " + str(random.randint(1, 9))
        invalid_matching_filenname = "Episode 100"

        self.record.store(valid_matching_filename)
        
        self.assertFalse(self.record.is_match(invalid_matching_filenname))
