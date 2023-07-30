import unittest
from module.watcher import Watcher
from module.record import Record
from module.util import Util
import os
import shutil

class TestWatcher(unittest.TestCase):
    '''This is not a full integration test. File are copied using shutil.copy'''

    def setUp(self):
        allowed_exts = ['.txt']
        self.record = Record('test.db')
        self.src_path = 'src_test/'
        self.dest_path = 'dest_test/'

        self.watcher = Watcher(self.src_path, 
                               self.dest_path, 
                               allowed_exts, 
                               self.record, 
                               debug_mode = True)
        
        self.record.open()
        self.record.close()

        os.mkdir(self.src_path)
        os.mkdir(self.dest_path)

    def tearDown(self):
        os.remove('test.db')
        shutil.rmtree(self.src_path)
        shutil.rmtree(self.dest_path)

    def test_explore_directory_copy_file(self):
        path_to_src_file = self.src_path + 'test.txt'
        open(path_to_src_file, 'w').close() # Create test file

        # Debug mode use copy instead of Rclone
        self.watcher.explore_directory(self.src_path) 

        path_to_dest_file = self.dest_path + 'test.txt'
        file_exist_in_dest_dir = os.path.isfile(path_to_dest_file)
        self.assertTrue(file_exist_in_dest_dir)
     
    def test_explore_directory_copy_subdirectory_file(self):
        src_subdir_path = self.src_path + 'folderB'
        os.mkdir(src_subdir_path)

        path_to_src_file = src_subdir_path + '/test.txt'
        open(path_to_src_file, 'w').close() # Create test file

        # Debug mode use copy instead of Rclone
        self.watcher.explore_directory(self.src_path) 

        path_to_dest_file = self.dest_path + 'test.txt'
        file_exist_in_dest_dir = os.path.isfile(path_to_dest_file)
        self.assertTrue(file_exist_in_dest_dir)