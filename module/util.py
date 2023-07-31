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
        path_to_dest_file = dest_path + Util.sanitize_filename_for_rclone(sanitize_filename(filename))

        return path_to_dest_file

    @staticmethod
    def generate_path_to_src_file(src_path, filename):
        path_to_file = src_path + str(filename)
        return path_to_file
    
    @staticmethod
    def sanitize_filename_for_rclone(filename):
        invalid_chars = ["'", '"'] # ' interfere with rclone commands
        safe_char = "i" # Best safest character to replace with

        sanitized_filename = str(filename)

        for invalid_char in invalid_chars:
            sanitized_filename = sanitized_filename.replace(invalid_char, safe_char)

        sanitized_filename = sanitize_filename(sanitized_filename)
        return sanitized_filename