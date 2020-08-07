import dbm  # database library
"""
import getpass  # console input hiding, may come back to this later
"""


def check_if_blank(x):
    #  returns True if value is None or blank
    if x in (None, ''):
        return True
    else:
        return False


def password_input_confirm(p1, p2):
    #  returns True if password inputs match for user creation
    if p1 == p2 and check_if_blank(p1) is False:
        return True
    else:
        return False


def authenticate(u, p):
    #  returns True if entered credentials match stored credentials
    with dbm.open('credentials', 'r') as c:
        if c[u].decode("utf-8") == p:
            #  decodes bytes retrieved from database value
            c.close()
            return True
        else:
            return False


action_type = input('Select Option: \n 1. Login\n 2. Create Account\n')
if action_type == '1':
    username = input('Username: ')
    password = input('Password: ')
    with dbm.open('credentials', 'r') as cred:
        #  open database in readonly mode
        if authenticate(username, password) is True:
            print('Authenticated')
        else:
            print('Failed to Authenticate')
elif action_type == '2':
    username = input('Username: ')
    password = input('Password: ')
    confirm_password = input('Password: ')
    if password_input_confirm(password, confirm_password) is True:
        with dbm.open('credentials', 'c') as cred:
            #  open database in mode to create and update entries
            cred[username] = password
            cred.close()
    else:
        print('Passwords do not match, or are blank.')
        #  TODO find way to return mismatched input passwords back to initial prompt.
else:
    print('Invalid option entered.')
    #  TODO find a way to return invalid option input back to initial prompt.
