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
                return

        logging.info(f"Command: {copy_command}")

        p = subprocess.Popen(
            copy_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            text=True
        )

        try:
            stdout, _ = p.communicate(timeout=3600)  # 1 hour
        except subprocess.TimeoutExpired:
            p.kill()
            stdout, _ = p.communicate()  # clean up remaining output
            record.set_error(file_id, "Transfer timed out")
            return

        return_code = p.returncode

        if return_code != 0:
            error_msg = (
                f"Error: {file_transfer_tool} exited with non-zero status "
                f"filename: {path_to_file}, errorcode: {return_code}"
            )
            logging.debug(error_msg)
            logging.debug("STDOUT: " + stdout)
            logging.debug("Error command: " + copy_command)
            record.set_error(file_id, error_msg)
            return
        else:
            logging.info(f"Copied {path_to_file} to {path_to_dest}")
            record.mark_as_finished(file_id)
            return

    @staticmethod
    def generate_rclone_copy_commands(path_to_file, path_to_dest):
        copy_rclone_command = "rclone copyto " + "'" + path_to_file + "' " + "'" + path_to_dest + "'" + " --log-file=yuki_rclone.log"
        return copy_rclone_command
    
    @staticmethod
    def generate_rsync_copy_commands(path_to_file, path_to_dest):
        copy_rsync_command = (
            f"rsync -av --progress --partial "
            f"--log-file=yuki_rsync.log --stats --itemize-changes "
            f"--timeout=60 --delay-updates "
            f"'{path_to_file}' '{path_to_dest}' "
            f">> yuki_rsync.log 2>&1"
        )
        return copy_rsync_command
