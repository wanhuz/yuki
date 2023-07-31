from module.record import Record
import sys

class Cli:
    def __init__(self, record : Record):
        self.__RECORD = record

    @property
    def record(self):
        return self.__RECORD
    
    def start(self):
        self.enter_interactive_sessions()

    def enter_interactive_sessions(self):
        
        while (True):
            instructions = "Choose an options:\n"
            options = "\na) Add new entry \nd) Remove entry \nf) Find entry \np) Print all \nt) Print last 50 record \ne) Exit\n"

            print(instructions, options)

            option_choosen = input()
            
            match option_choosen:
                case "e":
                    sys.exit(0)
                case "a":
                    self.add_filename_screen()
                case "d":
                    self.remove_filename_contains_screen()
                case "f":
                    self.search_filename_screen()
                case "p":
                    self.print_all_screen()
                case "t":
                    self.print_last_50_screen()

    def print_all_screen(self):
        self.record.open()
        self.record.print_all()
        self.record.close()

    def print_last_50_screen(self):
        self.record.open()
        self.record.print_last_50()
        self.record.close()

    def add_filename_screen(self):
        instruction = '\nAdd filename to record: \n'
        options = '\nb) Back\ne) Exit\n'

        while (True):
            print(instruction, options)
            user_input = input()

            match user_input:
                case "b":
                    break
                case "e":
                    sys.exit(0)
                case _:
                    self.record.open()
                    self.record.store(user_input)
                    self.record.close()
                    print('Successfully added ', user_input, ' to records!')

    def search_filename_screen(self):
        instruction = '\nSearch filename in record: \n'
        options = '\nb) Back\ne) Exit\n'

        while (True):
            print(instruction, options)
            user_input = input()

            match user_input:
                case "b":
                    break
                case "e":
                    sys.exit(0)
                case _:
                    self.record.open()
                    searched = self.record.search_contains(user_input)
                    self.record.close()

                    if (searched):
                        for search in searched:
                            print(search)
                    else:
                        print('No entry found for ', user_input)

    def remove_filename_contains_screen(self):
        instruction = '\nInput filename to search to delete: \n'
        options = '\nb) Back\ne) Exit\n'

        while (True):
            print(instruction, options)
            user_input = input()

            match user_input:
                case "b":
                    break
                case "e":
                    sys.exit(0)
                case _:  
                    self.remove_filename_search_if_exists(user_input)

    def remove_filename_search_if_exists(self, user_filename_input):
        self.record.open()
        search_result = self.record.search_contains(user_filename_input)
        self.record.close()

        if (len(search_result) > 0):
            for search in search_result: 
                print(search)

            self.remove_filename_contains_confirmation_screen(user_filename_input)
            return
        
        print('Nothing found for ' + user_filename_input)

    def remove_filename_contains_confirmation_screen(self, user_filename_input):
        print('\nAre you sure you want to delete these records? (y/n)')

        user_input_confirmation = input()
        if (user_input_confirmation == 'y'):
            self.record.open()
            self.record.delete_contains(user_filename_input)
            self.record.close()

            print('Successfully deleted ' + user_filename_input)