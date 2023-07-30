from module.record import Record
from module.util import Util
from module.remote import Remote
import os
import logging

logging.basicConfig(
    filename="yuki.log", 
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Watcher:

    def __init__(self, watch_dir, dest_path, exts : list, record : Record):
        self.__WATCH_DIR = watch_dir
        self.__EXTS = exts
        self.__RECORD = record
        self.__DEST_PATH = dest_path # example: "\"/home/user/test\"" with quote

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

    def start(self):
        self.explore_directory(self.watch_dir)

    #Explore file and copy from src to dest. Breaks if folder/dir is empty
    def explore_directory(self, folder):
        for file in os.listdir(folder):
            
            #file_obj refers to directory or file
            is_new_file_obj = self.is_new_file_obj(file)
            
            if (is_new_file_obj):
                        
                self.record.open()
                self.record.store(file)
                self.record.close()

                # check if file match extension
                if (self.filename_match_allowed_exts(file)): #if file is mkv, download
                    logging.info("Copying " + file + " over to destination directory")
        
                    path_to_file = folder + str(file)
                    Remote.copyto(path_to_file, self.dest_path)
                    continue

                # Check if file or directory
                if (Util.is_file(file)):
                    logging.info("Found but not matching extensions: " + file)
                    continue          
                else: #else file is a folder, explore it
                    pathtoDir = folder + file + "/"
                    self.explore_directory(pathtoDir)
                    
            else:
                continue
      
    
    def is_new_file_obj(self, filename):
        '''Return True if file or directory does not exists in record'''
        
        self.record.open()

        if (self.record.is_match(filename)):
            file_is_new = False
        else:
            file_is_new = True

        self.record.close()

        return file_is_new

    def filename_match_allowed_exts(self, filename):
        extension = Util.get_extension(filename)

        if extension in self.exts:
            return True
        return False