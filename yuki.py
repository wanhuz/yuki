import sys
from module.controller import Controller

def main(*args):

    if (len(sys.argv) == 1):
        print('Invalid commands! Run with --help to view all commands')
        return
    
    args = sys.argv[1:]

    if (args[0] == "run"):
        controller = Controller()
        controller.run()
    elif (args[0] == "cli"):
        controller = Controller()
        controller.interactive()
    elif (args[0] == "--help"):
        print('Arguments: \n\nrun - execute yuki script\ncli - enter interactive session to view records, add or delete')
    else:
        print('Invalid commands! Run with --help to view all commands')

if __name__ == "__main__":
    main()