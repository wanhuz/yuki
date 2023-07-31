# yuki

What's this?

A small script to watch a directory and then transfer files using rclone, then it record the file into small database so that the next time the script run, it won't transfer the file again.
Also works with file inside a directory.
In simple terms, it transfer all files from one directory (including subdirectory files inside it) into remote drives directory

To run
1. Install Python 3.7 or above
2. Clone this repository
3. Run "pip install -r requirements.txt" inside this directory
4. Copy .env.example into .env and edit it to your specifications. (Make sure src_path and dest_path exists!)
6. Execute using python, "python yuki.py run" to run the script or "python yuki.py cli" to enter interactive session (view record, delete, etc)

Things to take note

This script tracks whether file has been transferred or not using filename. So if a directory A has "episode 4.mkv" and directory B has also "episode 4.mkv". Only one "episode 4.mkv" will be transferred.
