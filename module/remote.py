import subprocess
import logging

logging.basicConfig(
    filename="yuki.log", 
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Remote:

    @staticmethod
    def copyto(src_path, dest_path):
        logging.info('Rclone copying ' + src_path + " to " + dest_path)

        copy_rclone_command = ['rclone', 'copyto', "\"", src_path, " ", "\"", dest_path, "\"", " --log-file=yuki_rclone.log"]
        subprocess.run(copy_rclone_command)