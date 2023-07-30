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

    @staticmethod
    def generate_rclone_copy_commands(path_to_file, path_to_dest):
        path_to_file = f'"{path_to_file}"'
        path_to_dest =  f'"{path_to_dest}"'
        log_command = "--log-file=yuki_rclone.log"
        copy_rclone_command = ['rclone', 'copyto', str(path_to_file), str(path_to_dest), str(log_command)]
        return copy_rclone_command