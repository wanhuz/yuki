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
        if path.isfile(filename):
            return True
        return False
