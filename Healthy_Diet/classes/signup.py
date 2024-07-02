import hashlib
from getpass import getpass
import json
from colorama import *
userInfo = "userInfo.json"

def loadDatabase(filepath):
    '''Load JSON file to read it'''
    try:
        with open(filepath, "r", encoding='UTF-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return print("The file doesn't exist") 

def hashingPassword(password:str):
    '''This function hashing the password using SHA256 '''
    passwordBytes= password.encode('utf-8')
    hashedPassword = hashlib.sha256(passwordBytes).hexdigest()
    return hashedPassword
    
    
def validate_input(password_length) :
    ''' Check if the length of password in valid '''
    try:
        if len(password_length) <= 8 :
            raise ValueError("Password length must be between 8 and 16")
        return password_length
    except ValueError:
        return  print("INVALID_LENGTH_MESSAGE")
    
    
def user_exists(username):
    ''' Check if the user exist in JSON file or not'''
    try:
        with open("userInfo.json", "r") as f:
            data= json.load(f)
            if username in data:    
                    return True
    except FileNotFoundError as fl_err:
        print(f"There is no file called {userInfo}")
    return False


def saveUserRegistration(username, hashedPW):
    '''Save user registration on JSON file'''
    userInfo = "userInfo.json"
    data = loadDatabase(userInfo)
    if data is None:
        data = {}
    if username in data:
        print(Fore.RED+ f"Username {username} already exists!" + Style.RESET_ALL)
    else:
        data[username] = hashedPW
        with open(userInfo, "w",encoding='UTF-8' ) as f:
            json.dump(data, f, indent=4)
            print(Fore.GREEN+ f"User {username} created successfully!" + Style.RESET_ALL) 

#TODO: fix input validation for username and password
#TODO: fix Validate input 
def register():
    username = input("Enter Your name to signUp: ")
    if user_exists(username):
        print("User already exists.")
        return
    passwordInput = input("Enter your new password to signUp: ")
    validatePW = validate_input(passwordInput)
    hashed_password = hashingPassword(validatePW)
    saveUserRegistration(username, hashed_password)

user_exists("Abdul")
# register()
# while True:
#     username= input("Enter your name: ")
#     passwordInput = input("enter your password: ")
#     if user_exists(username):
#         print("User already exist !!")
#         return
#     if username == "" and passwordInput == "":
#         raise ValueError("Username and Password can not be empty")
#     else:
#         hashingPW = hashingPassword(passwordInput)
#         saveUserRegistration(username, hashingPW)
#     continue



