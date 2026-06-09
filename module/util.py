from os import path
from os.path import isfile
from pathvalidate import sanitize_filename

class Util:
    @staticmethod
    def get_extension(filename : str):
        _, extension = path.splitext(filename)

        if (extension):
            return extension.lower()
        return False # No extension
    
    @staticmethod
    def is_file(path, filename):
        path_to_file = path + filename
        return isfile(path_to_file)

    @staticmethod
    def generate_path_to_dest_file(dest_path, filename):
        sanitized_filename = sanitize_filename(str(filename))
        
        path_to_dest_file = dest_path
        return path_to_dest_file

    @staticmethod
    def generate_path_to_src_file(src_path, filename):

        return src_path
    
    @staticmethod
    # Escape quote inside bash as bash command is literal
    def escape_quotes_parser(filename):
        # Solution: https://stackoverflow.com/a/48352047
        single_quote = "'"
        double_quote = '"' 
        escape_single_quote = r"'\''"
        escape_double_quote = r'"\""'

        if (single_quote in filename):
            sanitized_filename = filename.replace(single_quote, escape_single_quote)
        elif (double_quote in filename):
            sanitized_filename = filename.replace(double_quote, escape_double_quote)
        else:
            sanitized_filename = filename

        return sanitized_filename
    