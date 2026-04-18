import subprocess
import logging
import time

from module.record import Record

logging.basicConfig(
    filename="yuki.log", 
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - %(levelname)s - %(message)s')

class Remote:

    @staticmethod
    def copyto(record : Record, file_id, path_to_file, path_to_dest, file_transfer_tool = "rsync"):
        
        match file_transfer_tool:
            case "rsync":
                copy_command = Remote.generate_rsync_copy_commands(path_to_file, path_to_dest)
            case "rclone":
                copy_command = Remote.generate_rclone_copy_commands(path_to_file, path_to_dest)
            case _:
                logging.debug("Unknown file transfer tool: " + file_transfer_tool)
                record.set_error(file_id, "Unknown file transfer tool: " + file_transfer_tool)

        p = subprocess.Popen(copy_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        while p.poll() is None:
            time.sleep(1)

        if (p.returncode):
            error_msg = "Error, : " + file_transfer_tool + " exited with non-zero status, filename: " + path_to_file + ", errorcode: " + str(p.returncode)
            logging.debug(error_msg)
            logging.debug("STDOUT: " + str(p.stdout))
            logging.debug("Stderr:" + str(p.stderr))
            logging.debug("Error command: " + "' " + copy_command + " '")
            record.set_error(file_id, error_msg)
        else:
            logging.info("Copied " + path_to_file + " to " + path_to_dest)
            record.mark_as_finished(file_id)

    @staticmethod
    def generate_rclone_copy_commands(path_to_file, path_to_dest):
        copy_rclone_command = "rclone copyto " + "'" + path_to_file + "' " + "'" + path_to_dest + "'" + " --log-file=yuki_rclone.log"
        return copy_rclone_command
    
    @staticmethod
    def generate_rsync_copy_commands(path_to_file, path_to_dest):
        copy_rsync_command = (
            f"rsync -av --progress --partial --log-file=yuki_rsync.log "
            f"'{path_to_file}' '{path_to_dest}'"
        )
        return copy_rsync_command
