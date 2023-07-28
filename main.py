import sys
from module.controller import Controller
from dotenv import load_dotenv
import os

def load_controller_env():
    load_dotenv()

    record_path = os.getenv("RECORD_PATH")
    src_path = os.getenv("SRC_PATH")
    dest_path = os.getenv("DEST_PATH")
    allowed_exts_list = os.getenv("ALLOWED_EXTENSION_LIST")

    return Controller(record_path,
                        src_path,
                        dest_path,
                        allowed_exts_list)

def main():
    args = sys.argv[1:]

    if (args[0] == "run"):
        controller = load_controller_env()
        controller.run()
    elif (args[0] == "cli"):
        print('cli')
    else:
        print('Invalid commands')

if __name__ == "__main__":
    main()