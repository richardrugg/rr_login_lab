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


def new_password_valid(cp, np):
    #  returns True if current password and new password are not the same, or blank
    if cp != np and check_if_blank(np) is False:
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


def login():
    #  performs actual login based on returns from other checks
    print('\nLogin Prompt: ')
    u = input('Username: ')
    p = input('Password: ')
    with dbm.open('credentials', 'r') as c:
        #  opens database in mode to create and update entries
        if authenticate(u, p) is True:
            print('Successfully Authenticated!\n')
            #  would obviously point this to something more useful
        else:
            print('Invalid Username / Password.\n')
            login_process()


def login_verify(u, p):
    #  returns True if login credentials are valid, without logging in
    with dbm.open('credentials', 'r') as c:
        #  opens database in mode to create and update entries
        if authenticate(u, p) is True:
            return True
        else:
            return False


def account_create():
    #  creates new account
    print('\nAccount Creation: ')
    username = input('Username: ')
    password = input('Password: ')
    confirm_password = input('Password: ')
    if password_input_confirm(password, confirm_password) is True:
        with dbm.open('credentials', 'c') as cred:
            #  open database in mode to create and update entries
            if cred.get(username) is None:
                #  confirm username does not already exist in database
                cred[username] = password
                #  add username and password to database
                print('Account Created!\n')
                login_process()
            else:
                print('Account already exists!')
                account_create()
    else:
        print('Passwords do not match, or are blank. Please try again.\n')
        account_create()


def change_password():
    #  changes password of existing account
    print('\nChanging Password: ')
    u = input('Username: ')
    cp = input('Current Password: ')
    np = input('New Password: ')
    cnp = input('Confirm New Password: ')
    if new_password_valid(cp, np) is True and np == cnp and login_verify(u, cp) is True:
        #  confirm password is valid, credentials are valid and new passwords match
        with dbm.open('credentials', 'c') as c:
            #  open database in mode to create and update entries
            if c.get(u) is not None:
                #  confirms username exists in database
                c[u] = np
                #  updates password value of username key in database
                print('Password Successfully Changed.')
                c.close()
                #  this database close must be here so new passwords works with this next login_process call
                login_process()
            else:
                print('Incorrect Username / Password Combination!')
                change_password()
    else:
        print('Incorrect Username / Password Combination!')
        change_password()


def login_process():
    #  this is the main process that links everything together
    action_type = input('Select Option: \n 1. Login\n 2. Create Account\n 3. Change Password\n')
    if action_type == '1':
        #  login action
        login()
    elif action_type == '2':
        #  create account action
        account_create()
    elif action_type == '3':
        #  change password action
        change_password()
    else:
        print('Invalid option entered.\n')
        login_process()


login_process()
