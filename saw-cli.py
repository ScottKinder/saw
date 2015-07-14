from pprint import pprint
import os
import sys
sys.path.append(os.getcwd())
from saw import *

def main():
    user = None
    while True:
        #os.system('clear')
        print('1. Get auth token')
        print('2. View connected minions')
        print('3. Run command')
        print('4. Run state')
        print('5. Test targeting')
        print('6. Exit\n\n')
        choice = raw_input('Enter your choice: ')
        if choice == '1':
            if not user:
                user = user_session()
            if not user.auth_token:
                user.set_auth_token()
        elif choice == '2':
            if not user:
                user = user_session()
            if not user.auth_token:
                user.set_auth_token()
            minions = get_minions(user.auth_token)
            print_minions(minions)
            break
        elif choice == '3':
            command = raw_input('Command to run: ')
            target = raw_input('Target: ')
            print
            if not user:
                user = user_session()
            if not user.auth_token:
                user.set_auth_token()
            cmdrun = cmd_run(user.auth_token, target, command)
            print
            print_cmd_run(cmdrun)
            break
        elif choice == '3':
            state = raw_input('State to run: ')
            target = raw_input('Target: ')
            print
            if not user:
                user = user_session()
            if not user.auth_token:
                user.set_auth_token()
            states = run_state(user.auth_token, target, state)
            print
            print_run_state(states)
            break
        elif choice == '4':
            target = raw_input('Target: ')
            print
            if not user:
                user = user_session()
            if not user.auth_token:
                user.set_auth_token()
            test = test_target(user.auth_token, target)
            print('\n' + test)
            break
        elif choice == '5':
            break
        else:
            print('Invalid input.\n')
            time.sleep(2)

if __name__ == '__main__':
    main()
