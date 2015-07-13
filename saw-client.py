mport os
import sys
sys.path.append(os.getcwd())
from saw import *

def main():
    user = None
    while True:
        #os.system('clear')
        print('1. View connected minions')
        print('2. Run command')
        print('3. Run state')
        print('4. Exit\n\n')
        choice = raw_input('Enter your choice: ')
        if choice == '1':
            if not user:
                user = user_session()
            if not user.auth_token:
                user.set_auth_token()
            minions = get_minions(user.auth_token)
            print_minions(minions)
            break
        elif choice == '2':
            command = raw_input('cmd.run to run: ')
            target = raw_input('target: ')
            print
            if not user:
                user = user_session()
            returns = cmd_run(user.user_name, target, command)
            print
            print_cmd_run(returns)
            break
        elif choice == '3':
            command = raw_input('state to run: ')
            target = raw_input('target: ')
            print
            if not user:
                user = user_session()
            returns = run_state(user.user_name, target, state)
            print
            print_cmd_run(returns)
            break
        elif choice == '4':
            break
        else:
            print('Invalid input.\n')
            time.sleep(2)

if __name__ == '__main__':
    main()
