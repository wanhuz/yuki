import subprocess
import logging

logging.basicConfig(
    filename="yuki.log", 
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Remote:

    @staticmethod
    def copyto(path_to_file, path_to_dest):
        logging.info('Rclone copying ' + path_to_file + " to " + path_to_dest)

        copy_rclone_command = Remote.generate_rclone_copy_commands(path_to_file, path_to_dest)
        subprocess.run(copy_rclone_command)

    def generate_rclone_copy_commands(path_to_file, path_to_dest):
        copy_rclone_command = ['rclone', 'copyto', "\"", path_to_file, " ", "\"", path_to_dest, "\"", " --log-file=yuki_rclone.log"]
        return copy_rclone_command