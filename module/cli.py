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
            instructions = "Choose an options:\n\n"
            options = "a) Add new entry \n d) Remove entry \n f) Find entry \n e) Exit\n"

            print(instructions, options)

            option_choosen = input()
            
            match option_choosen:
                case "e":
                    sys.exit(0)
                case "a":
                    self.add_filename_screen()
                case "d":
                    self.remove_filename_screen()
                case "f":
                    self.search_filename_screen()
                case "p":
                    self.record.print_all()


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
                    searched = self.record.search(user_input)
                    self.record.close()

                    if (searched):
                        for search in searched:
                            print(search)
                    else:
                        print('No entry found for ', user_input)
                    

    def remove_filename_screen(self):
        instruction = '\nSearch filename to delete: \n'
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
                    self.record.delete_all(user_input)
                    self.record.close()
                    print('Successfully deleted ' + user_input)
