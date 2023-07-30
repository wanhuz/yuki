import subprocess
import logging
import time

logging.basicConfig(
    filename="yuki.log", 
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Remote:

    @staticmethod
    def copyto(path_to_file, path_to_dest):

        copy_rclone_command = Remote.generate_rclone_copy_commands(path_to_file, path_to_dest)
        p = subprocess.Popen(copy_rclone_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        while p.poll() is None:
            time.sleep(1)

        if (p.returncode):
            logging.debug("Error, : " + "rclone copyto" + " exited with non-zero status, filename: " + path_to_file + ", errorcode: " + str(p.returncode))
            logging.debug("STDOUT: " + str(p.stdout))
            logging.debug("Stderr:" + str(p.stderr))
            logging.debug("Rclone command: " + "' " + copy_rclone_command + " '")

    @staticmethod
    def generate_rclone_copy_commands(path_to_file, path_to_dest):
        copy_rclone_command = "rclone copyto " + "'" + path_to_file + "' " + "'" + path_to_dest + "'" + " --log-file=yuki_rclone.log"
        return copy_rclone_command