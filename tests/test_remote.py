import unittest
from module.remote import Remote

class TestRemote(unittest.TestCase):

    def test_valid_rclone_copyto_commands(self):
        valid_path_to_file = "/home/user/media/file.mkv"
        valid_path_to_dest_file = "Drive:foldername/file.mkv"
        valid_rclone_copyto_commands = f"rclone copyto '{valid_path_to_file}' '{valid_path_to_dest_file}' --log-file=yuki_rclone.log"

        rclone_copyto_commands = Remote.generate_rclone_copy_commands(valid_path_to_file, valid_path_to_dest_file)

        self.assertEqual(rclone_copyto_commands, valid_rclone_copyto_commands)