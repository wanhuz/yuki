from module.record import Record
from module.watcher import Watcher
from module.cli import Cli
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(
    filename="yuki.log", 
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Controller:

    def __init__(self, dry_run = False):
        load_dotenv()

        record_path = os.getenv("RECORD_PATH")
        src_path = os.getenv("SRC_PATH")
        dest_path = os.getenv("DEST_PATH")
        allowed_exts_list = os.getenv("ALLOWED_EXTENSION_LIST")
        file_transfer_tool = os.getenv("FILE_TRANSFER_TOOL")
        debug_mode = os.getenv("DEBUG_MODE")

        self.__RECORD = Record(record_path)
        self.__WATCHER = Watcher(src_path, 
                                 dest_path, 
                                 allowed_exts_list, 
                                 self.__RECORD,
                                 debug_mode=debug_mode,
                                 dry_run = dry_run,
                                 file_transfer_tool = file_transfer_tool)
        self.__CLI = Cli(self.record)
    
    @property
    def record(self):
        return self.__RECORD
    
    @property
    def watcher(self):
        return self.__WATCHER
    
    @property
    def cli(self):
        return self.__CLI
        
    def run(self):
        self.watcher.start()

    def interactive(self):
        self.cli.start()