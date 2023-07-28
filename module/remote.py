import logging
import os
import shutil
from pathvalidate import sanitize_filename

logging.basicConfig(
    filename="move-once.log", 
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Remote:

    def __init__(self, dest_path):
        self.__DEST_PATH = dest_path # example: "\"/home/user/test\"" with quote

    @property
    def dest_path(self):
        return self.__DEST_PATH

    def lock(self):
        logging.info("Locking destination directory")

        lock_filename = 'lock.txt'
        lock_filepath = self.dest_path + lock_filename

        open(lock_filepath, 'w').close()

    def unlock(self):
        logging.info("Locking destination directory")

        lock_filename = 'lock.txt'
        lock_filepath = self.dest_path + lock_filename

        os.remove(lock_filepath) #break if file does not exist

    def copy(self, src_filepath):
        logging.info("Copying " + src_filepath + " to " + self.dest_path)

        shutil.copy(src_filepath, self.dest_path)