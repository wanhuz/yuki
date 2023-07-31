from os import path
from pathvalidate import sanitize_filename

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

    @staticmethod
    def generate_path_to_dest_file(dest_path, filename):
        sanitized_filename = sanitize_filename(str(filename))
        
        path_to_dest_file = dest_path + Util.escape_quotes_parser(sanitized_filename)
        return path_to_dest_file

    @staticmethod
    def generate_path_to_src_file(src_path, filename):
        filename = Util.escape_quotes_parser(filename)
        path_to_file = src_path + filename
        return path_to_file
    
    @staticmethod
    # Escape quote inside shell commands
    def escape_quotes_parser(filename):
        single_quote = "'"
        double_quote = '"' # ' interfere with rclone commands
        escape_single_quote = r"'\''" # Best safest character to replace with
        escape_double_quote = r'"\""'

        if (single_quote in filename):
            sanitized_filename = filename.replace(single_quote, escape_single_quote)
        elif (double_quote in filename):
            sanitized_filename = filename.replace(double_quote, escape_double_quote)
        else:
            sanitized_filename = filename

        return sanitized_filename
    