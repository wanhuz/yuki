# yuki

What's this?

A small script to watch a directory and then transfer files using rclone, then it record the file into small database so that the next time the script run, it won't transfer the file again.
Also works with file inside a directory.
In simple terms, it transfer all files from one directory (including subdirectory files inside it) into remote drives directory

Things to take note

This script tracks whether file has been transferred or not using filename. So if a directory A has "episode 4.mkv" and directory B has also "episode 4.mkv". Only one "episode 4.mkv" will be transferred.
