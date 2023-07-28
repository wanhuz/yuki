from module.remote import Remote
from module.record import Record
from module.watcher import Watcher
import logging
from pathvalidate import sanitize_filename

logging.basicConfig(
    filename="move-once.log", 
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

remote = Remote("dest/")
record = Record("history.db")
watcher = Watcher("src/", 'dest/', ['.txt', '.avi', '.mp4'], record)
      
#Main
watchdir = "src/"
watcher.start()