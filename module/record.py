
import sqlite_utils
import logging


logging.basicConfig(
    filename="move-once.log", 
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Record:

    def __init__(self, filename):
        self.__DB_FILENAME = filename

    @property
    def db_table(self):
        return self.__DB_TABLE
    
    def open(self):
        self.__DB = sqlite_utils.Database(self.__DB_FILENAME)
        self.__DB_TABLE = self.__DB["filename"]
    
    def close(self):
        self.__DB.close()
    
    def store(self, filename):
        logging.info('Storing ' + filename + ' into database')
        self.db_table.insert({"name" : filename}, pk="rowid")
        
    def print_all(self):
        filenames = self.db_table.rows
        for filename in filenames:
            print(filename)
    
    def is_match(self, filename) -> bool:
        rows = self.db_table.rows_where("name = ?", [filename])
    
        if any(rows):
            logging.info('Match found of filename: ' + filename)
            return True
        return False