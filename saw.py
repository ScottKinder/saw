from getpass import getpass
import re
import requests

class user_session:
    def __init__(self, user_name=None):
        '''
        Initializer. Optionally takes user_name(str).
        '''
        self.auth_token = None

        if not user_name:
            self.user_name = raw_input('Username: ')
        else:
            self.user_name = user_name

    def set_auth_token(self, user_pass=None):
        '''
        sets instance variable for auth_token that allows x-auth-token header
        authentication with salt-api. Optionally takes user_pass(str).
        '''
        if not user_pass:
            data = {'username': self.user_name, 'password': get_pw(), 'eauth': 'pam'}
        else:
            data = {'username': self.user_name, 'password': user_pass, 'eauth': 'pam'}

        r = requests.post('https://den-prod-salt01.clickbank.local/login', data=data)

        try:
            self.auth_token = r.headers['x-auth-token']
            self.auth_expiry = re.search(r'expires=(.*);', r.headers['set-cookie']).group(1)
        except:
                print('Auth error.')

def get_pw():
    '''
    prompt for password as needed
    '''
    return getpass('Kerberos password: ')

def cmd_run(user, target, cmd, silent=True, user_pass=None):
    '''
    Runs cmd.run from state parameter. Takes user(str), target(str),
    cmd(str). Optionally takes silent(bool) and user_pass(str).
    Returns dict of results per minion.
    '''
    if not user_pass:
        data = {'username': user, 'tgt': target, 'client': 'local', 'eauth': 'pam', 'password': get_pw(), 'fun': 'cmd.run', 'arg': cmd }
    else:
        data = {'username': user, 'tgt': target, 'client': 'local', 'eauth': 'pam', 'password': user_pass, 'fun': 'cmd.run', 'arg': cmd }

    r = requests.post("https://den-prod-salt01.clickbank.local/run", data=data)
    returns = r.json()['return'][0]

    if r.status_code != 200:
        print('Status code not 200, something probably went wrong.')
        print(r.status_code)
        pprint(r.json())
    else:
        return returns

def print_cmd_run(cmd):
    '''
    prints returned dict from cmd_run function
    '''
    for minion in cmd:
        print('*** ' + minion + ' ***\n')
        print(cmd[minion] + '\n')
        print('-' * 10 + '\n')

def get_minions(auth_token, url='https://den-prod-salt01.clickbank.local/minions'):
    '''
    returns dict of minions that were connected when function was run, uses
    x-auth-token header value for authentication.
    '''
    headers = {'X-Auth-Token': auth_token}
    r = requests.get(url, headers=headers)
    minions = r.json()['return'][0]
    return minions

def print_minions(minions):
    '''
    prints dict of minions from get_minions function.
    '''
    print('Registered minions:\n')
    for minion in minions:
        print('* ' + minion)
        print('  Kernel release: %s\n') % minions[minion]['kernelrelease']
    print('-' * 10 + '\n')

def run_state(user, target, state, url='https://den-prod-salt01.clickbank.local/run', pillar=None, user_pass=None):
    '''
    runs a state.sls where target is the path to the state. pillar can be a string
    in the form of pillar='pillar={"value1": "string"}'.
    returns dict with return information from the salt-api about the states run
    from the state file specified.
    '''
    if not user_pass:
        if pillar:
            data = {'username': user, 'tgt': target, 'client': 'local', 'eauth': 'pam', 'password': get_pw(), 'fun': 'state.sls', 'arg': [state, pillar] }
        else:
            data = {'username': user, 'tgt': target, 'client': 'local', 'eauth': 'pam', 'password': get_pw(), 'fun': 'state.sls', 'arg': [state] }
    else:
        if pillar:
            data = {'username': user, 'tgt': target, 'client': 'local', 'eauth': 'pam', 'password': user_pass, 'fun': 'state.sls', 'arg': [state, pillar] }
        else:
            data = {'username': user, 'tgt': target, 'client': 'local', 'eauth': 'pam', 'password': user_pass, 'fun': 'state.sls', 'arg': [state] }

    r = requests.post(url, data=data)
    results = r.json()['return'][0]
    return results

def print_run_state(state):
    '''
    prints dict from run_state function
    '''
    for minion in state:
        print('*** ' + minion + ' ***\n')
        for item in state[minion]:
            try:
                comment = state[minion][item]['comment']
                result = str(state[minion][item]['result'])
                print('State: ' + item)
                print('Comment: ' + comment)
                print('Result: ' + result + '\n')
            except:
                print(state[minion][0] + '\n')
