import dbm  # database library
#  import getpass  # console input hiding, may come back to this later


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
        u2 = c.get(u)
        #  u2 created to get value of username as key
        if u2 is None:
            #  checks if u2 is None (doesn't exist in database)
            return False
        elif c[u].decode("utf-8") == p:
            #  decodes bytes retrieved from database value
            return True
        else:
            return False


def login(u, p):
    with dbm.open('credentials', 'r') as c:
        if authenticate(u, p) is True:
            print('Successfully Authenticated!\n')
            c.close()
        else:
            print('Invalid Username / Password.\n')
            c.close()
            login_process()


def login_process():
    global action_type
    action_type = input('Select Option: \n 1. Login\n 2. Create Account\n')
    if action_type == '1':
        username = input('Username: ')
        password = input('Password: ')
        login(username, password)
    elif action_type == '2':
        username = input('Username: ')
        password = input('Password: ')
        confirm_password = input('Password: ')
        if password_input_confirm(password, confirm_password) is True:
            with dbm.open('credentials', 'c') as cred:
                #  open database in mode to create and update entries
                cred[username] = password
                print('Account Created!\n')
                login_process()
        else:
            print('Passwords do not match, or are blank.\n')
            login_process()
    else:
        print('Invalid option entered.\n')
        login_process()


login_process()
