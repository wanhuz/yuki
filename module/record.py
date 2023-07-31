
import sqlite_utils
import logging


logging.basicConfig(
    filename="yuki.log", 
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

    def print_last_50(self):
        MAX_PRINT = 50
        i = 0

        filenames = self.db_table.rows_where(order_by="rowid desc")
        filenames_reversed = [filename for filename in filenames].reverse()

        for filename in filenames_reversed:
            print(filename)
            i += 1
            if (i > MAX_PRINT):
                break
            
    def search(self, name) -> list:
        searchedList = []

        rows = self.db_table.rows_where("name = ?", [name])
        check_for_empty = self.db_table.rows_where("name = ?", [name])

        try:
            next(check_for_empty)
        except StopIteration:
            return []
        
        searchedList = [row for row in rows] #Convert to list
        return searchedList

    def delete_all(self, name):
        rows = self.db_table.rows_where("name = ?", [name])
        
        for row in rows:
            self.db_table.delete(row["rowid"])
            
        logging.info('Deleted ' + name)
    
    def is_match(self, filename) -> bool:
        rows = self.db_table.rows_where("name = ?", [filename])
    
        if any(rows):
            return True
        return False