#! python3

#A VERY insecure password manager

# Import modules
import sys
import pyperclip
import json
import pprint
import getpass


# Global variable definitions
pw = {}

def print_menu():
    print("""Password Store Menu:
l: List all accounts
a: Add an account
e: Edit an account
d: Delete an account
c: Copy account password
m: Print this menu
q: Quit
    """)


def save_data(pw):
    """Write password data to a file
    
    Arguments: Item to save to file
    """
    try:
        with open('pw.data', mode='w') as pw_data:
            json.dump(pw,pw_data)
            save_result = True
    except(IOError):
        print('File save error!')
        save_result = False
    return save_result


def load_data():
    """Read password data in from file.

    Arguments: None
    """
    global pw
    try:
        """Read blockchain data file and load it into blockchain object"""
        with open('pw.data', mode='r') as pw_data:
            pw = json.load(pw_data)
    except(IOError):
        # data file doesn't exist, so fill it with sample data
        pw = {"aol": "qwertyu",
            "mail": "tyuio",
            "facebook": "sdfghj",
            "insta": "cvbnm"
            }


load_data()

def add_account(pw):
    """Add a new account to the password dictionary.

    Arguments: Dictionary to add to
    """
    #global pw
    ret_value = False
    new_key = input("What is the account name? ")
    # Each account can only exist once in dictionary
    if new_key not in list(pw.keys()):
        # Get new password twice to make sure it is correct
        new_value1 = getpass.getpass("What is the password? ")
        new_value2 = getpass.getpass("Please re-enter the password: ")
        if new_value1 == new_value2:
            pw.update({new_key:new_value1})
            ret_value = True if save_data(pw) else False
        else:
            print("Passwords do not match.")
            ret_value = False
    else:
        print("That account already exists.")
        ret_value = False
    return ret_value

if len(sys.argv) < 2:
    print("Usage: pw.py [account] - copy account\'s password to clipboard")
    sys.exit(1)


account = sys.argv[1]
if account == "menu":
    print_menu()
    while True:
        menu_opt = input("What would you like to do? ")
        # Add a new account
        if menu_opt and menu_opt.upper() == "A":
            if not add_account(pw):
                print("Account not added.")
            else:
                print("Account added.")
                pprint.pprint(pw)
        # Copy account password to clipboard
        elif menu_opt and menu_opt.upper() == "C":
            account = input("Copy password for which account? ")
            if account in list(pw.keys()):
                pwToCopy = pw.get(account)
                pyperclip.copy(pwToCopy)
                print("Password copied to clipboard.")
            else:
                # Be nice and offer to add a new account
                addAccount = input("That account does not exist. Add it (y/n)?")
                if addAccount and addAccount.upper() in "Y":
                    if not add_account(pw):
                        print("Account not added.")
                    else:
                        print("Account added.")
                        print(pw)
        # List out accounts and passwords (show passwords during devel. Hide them later.)
        elif menu_opt and menu_opt.upper() == "L":
            pprint.pprint(pw)
        # Print menu
        elif menu_opt and menu_opt.upper() == "M":
            print_menu()
        # Quit
        elif menu_opt and menu_opt.upper() == "Q":
            print("Ok. Goodbye.")
            break

