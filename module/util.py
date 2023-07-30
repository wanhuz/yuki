from os import path

class Util:
    @staticmethod
    def get_extension(filename : str):
        _, extension = path.splitext(filename)

        if (extension):
            return extension.lower()
        return False # No extension

    @staticmethod
    def is_file(filename):
        # Check whether it is a file based on filename, not by whether it exist or not on system
        if (Util.get_extension(filename)): 
            return True
        return False
