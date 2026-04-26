from module.record import Record
from module.watcher import Watcher
from module.cli import Cli
import logging
from dotenv import load_dotenv
import os
import sys

if sys.platform.startswith("linux"):
    import fcntl
    import atexit

logging.basicConfig(
    filename="yuki.log", 
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Controller:

    def __init__(self, dry_run = False):
        load_dotenv()

        if sys.platform.startswith("linux"):
            self.lock_file_handle = None
            max_active_instance = int(os.getenv("MAX_ACTIVE_INSTANCE", 10))
            
            if not self.acquire_slot(MAX_INSTANCES=max_active_instance):
                print("Max instances reached, exiting")
                sys.exit(1)

            atexit.register(self.release_slot)

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

    def acquire_slot(self, LOCK_DIR="./locks", MAX_INSTANCES=4):
        os.makedirs(LOCK_DIR, exist_ok=True)

        for i in range(MAX_INSTANCES):
            path = f"{LOCK_DIR}/instance_{i}.lock"

            try:
                f = open(path, "w")
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)

                self.lock_file_handle = f
                return True

            except IOError:
                continue

        return False
    
    def release_slot(self):
        if self.lock_file_handle:
            try:
                fcntl.flock(self.lock_file_handle, fcntl.LOCK_UN)
                self.lock_file_handle.close()
            except:
                pass