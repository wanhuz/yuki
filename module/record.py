
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
        filenames = self.db_table.rows
        filenames_list = [filename for filename in filenames]

        if (len(filenames_list) > 50):
            for filename in filenames_list[-51:]:
                print(filename)
        else:
            for filename in filenames_list:
                print(filename)
    
    def search_contains(self, name) -> list:
        search_pattern = f"%{name}%"
        searchedList = []

        rows = self.db_table.rows_where("name LIKE ?", [search_pattern])
        check_for_empty = self.db_table.rows_where("name LIKE ?", [search_pattern])

        try:
            next(check_for_empty)
        except StopIteration:
            return []
        
        searchedList = [row for row in rows] #Convert to list
        return searchedList
    
    def is_match(self, filename) -> bool:
        rows = self.db_table.rows_where("name = ?", [filename])
    
        if any(rows):
            return True
        return False
    
    def delete_contains(self, name):
        search_pattern = f"%{name}%"
        rows = self.db_table.rows_where("name LIKE ?", [search_pattern])
        
        for row in rows:
            self.db_table.delete(row["rowid"])
            
        logging.info('Deleted ' + name)