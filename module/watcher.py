from module.record import Record
from module.util import Util
from module.remote import Remote
import os
import logging
import shutil

logging.basicConfig(
    filename="yuki.log", 
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Watcher:

    def __init__(self, watch_dir, dest_path, exts : list, record : Record, debug_mode = False):
        self.__WATCH_DIR = watch_dir
        self.__EXTS = exts
        self.__RECORD = record
        self.__DEST_PATH = dest_path
        self.__DEBUG_MODE = debug_mode

    @property
    def watch_dir(self):
        return self.__WATCH_DIR

    @property
    def exts(self):
        return self.__EXTS
    
    @property
    def record(self):
        return self.__RECORD
    
    @property
    def dest_path(self):
        return self.__DEST_PATH
    
    @property
    def debug_mode(self):
        return self.__DEBUG_MODE

    def start(self):
        self.explore_directory(self.watch_dir)

    #Explore file and copy from src to dest. Breaks if folder/dir is empty
    def explore_directory(self, folder):
        for filename in os.listdir(folder):

            if (Util.is_file(filename)):
                is_new_file = self.is_new_file(filename)

                if (is_new_file):

                    if (self.filename_match_allowed_exts(filename)):
                        
                        self.record.open()
                        self.record.store(filename)
                        self.record.close()

                        logging.info("Attempting to copy " + filename + " over to destination directory")
            
                        path_to_file = Util.generate_path_to_src_file(folder, filename)
                        path_to_dest_file = Util.generate_path_to_dest_file(self.dest_path, filename)
                        self.copy_once(path_to_file, path_to_dest_file, self.debug_mode)

                        logging.info('Finished copying for ' + filename)
                    
            else: 
                    path_to_new_dir = folder + filename + "/"
                    self.explore_directory(path_to_new_dir)
      
    
    def copy_once(self, path_to_file, path_to_dest_file, is_debug_mode):
        if (is_debug_mode):
            logging.debug('Copying ' + path_to_file + ' to ' + path_to_dest_file)
            
            shutil.copy(path_to_file, path_to_dest_file)
        else:
            Remote.copyto(path_to_file, path_to_dest_file)

    def is_new_file(self, filename):
        '''Return True if file or directory does not exists in record'''
        
        self.record.open()
        exist_in_record = self.record.is_match(filename)
        self.record.close()

        if (not exist_in_record):
            logging.info('New file found for ' + filename)
            return True
        return False

    def filename_match_allowed_exts(self, filename):
        extension = Util.get_extension(filename)

        if extension in self.exts:
            return True
        return False