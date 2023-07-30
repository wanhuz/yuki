import unittest
from module.remote import Remote

class TestRemote(unittest.TestCase):

    def test_valid_rclone_copyto_commands(self):
        valid_rclone_copyto_commands = ["rclone", "copyto", "\"/home/user/media/file.mkv\"", "\"Drive:foldername/file.mkv\"", "--log-file=yuki_rclone.log"]

        rclone_copyto_commands = Remote.generate_rclone_copy_commands("/home/user/media/file.mkv", "Drive:foldername/file.mkv")
        print(valid_rclone_copyto_commands)
        print(rclone_copyto_commands)

        self.assertEqual(rclone_copyto_commands, valid_rclone_copyto_commands)