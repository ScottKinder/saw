import os
import sys
import time
sys.path.append(os.getcwd())
from saw2 import *


def main():
    os.system('clear')
    user = user_session()
    user.set_auth_token()
    while True:
        print('1. View connected minions')
        print('2. Run command')
        print('3. Run state')
        print('4. Test target')
        print('5. Print auth token')
        print('6. Exit\n')
        print('Press \'c\' to clear the screen\n\n')
        choice = raw_input('Enter your choice: ')
        if choice == '1':
            if not user.auth_token:
                user.set_auth_token()
            minions = get_minions(user.auth_token)
            print_minions(minions)
        elif choice == '2':
            command = raw_input('Command to run: ')
            target = raw_input('Target: ')
            print
            cmdrun = cmd_run(user.user_name, target, command)
            print
            print_cmd_run(cmdrun)
        elif choice == '3':
            state = raw_input('State to run: ')
            target = raw_input('Target: ')
            if not user.auth_token:
                user.set_auth_token()
            print
            states = token_run_state(user.auth_token, target, state)
            print
            print_run_state(states)
        elif choice == '4':
            target = raw_input('Target: ')
            print
            if not user.auth_token:
                user.set_auth_token()
            test = test_target(user.auth_token, target)
            print('\n' + test)
        elif choice == '5':
            print('\nAuth token: ' + user.auth_token)
            print('Token expiry: ' + user.auth_expiry + '\n')
        elif choice == '6':
            break
        else:
            print('Invalid raw_input.\n')
            time.sleep(2)

if __name__ == '__main__':
    main()
