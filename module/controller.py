from module.record import Record
from module.watcher import Watcher
import logging
from pathvalidate import sanitize_filename

logging.basicConfig(
    filename="move-once.log", 
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Controller:

    def __init__(self, record_path, src_path, dest_path, allowed_exts_list):
        self.__RECORD = Record(record_path)
        self.__WATCHER = Watcher(src_path, 
                                 dest_path, 
                                 allowed_exts_list, 
                                 self.__RECORD)
    
    @property
    def record(self):
        return self.__RECORD
    
    @property
    def watcher(self):
        return self.__WATCHER
        
    def run(self):
        self.watcher.start()