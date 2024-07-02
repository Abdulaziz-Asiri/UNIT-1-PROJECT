import getpass as getpass
import signup 
from colorama import *
import json

userInfo = "userInfo.json"

def authenticate_user(username, password):
    with open(userInfo, "r") as f:
        data = json.load(f)
        if username in data:
            hashedPassword = signup.hashingPassword(password)
            if hashedPassword == data[username]:
                return True
        else:
            return False


def login():
    username = input("Enter username: ")
    if not signup.user_exists(username):
        print(Fore.RED+"User does not exist." + Style.RESET_ALL)
        return

    password = input("Password: ")
    if not authenticate_user(username, password):
        print(Fore.RED + "Incorrect password." + Style.RESET_ALL)
        return
    print(Fore.GREEN + "Login successful." + Style.RESET_ALL)


login()