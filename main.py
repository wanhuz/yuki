import sys
from module.controller import Controller

def main():
    args = sys.argv[1:]

    if (args[0] == "run"):
        controller = Controller()
        controller.run()
    elif (args[0] == "cli"):
        controller = Controller()
        controller.interactive()
    else:
        print('Invalid commands!')

if __name__ == "__main__":
    main()