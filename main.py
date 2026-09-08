from function.admin import admin_menu
from function.manager import manager_menu
from function.chef import chef_menu
from function.customer import customer_menu
import os

# Constants
MAX_LOGIN_ATTEMPTS = 3
DATA_FOLDER = "data"
USER_FILE = os.path.join(DATA_FOLDER, "user.txt")

# Ensure data directory exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Initialize user file if it doesn't exist
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as file:
        file.write("admin,admin123,admin,Admin User,1234567890,Admin Address,admin@example.com\n")

def decorate():
    print("\n" + " " * 28 + "-" * 29)
    print(" " * 28 + "* WELCOME TO PYTHON PROJECT *") 
    print(" " * 28 + "-" * 29)
    print("\nGroup Members: 1. Nirajan Adhikari  2. Anil Ghimire  3. Nandan Ghimire  4. Hari Sharma")
    print("><" * 42)
    print("\n" + " " * 27 + "-" * 32)
    print(" " * 27 + "* RESTAURANT MANAGEMENT SYSTEM *")
    print(" " * 27 + "-" * 32)
    print()

def login():
    attempts = 0
    while attempts < MAX_LOGIN_ATTEMPTS:
        username = input("Enter username: ")
        password = input("Enter password: ")
        with open(USER_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    uname, pwd, role = parts[0], parts[1], parts[2]
                    if uname == username and pwd == password:
                        return role, username
        attempts += 1
        print(f"Invalid username or password. {MAX_LOGIN_ATTEMPTS - attempts} attempts remaining.")
    print("Access denied due to too many attempts.")
    return None, None

def menu():
    while True:
        print('\n'+ "-"*50)
        print("Welcome to our hotel! Here is our menu")
        print('\n''1. Admin')
        print('2. Manager')
        print('3. Chef')
        print('4. Customer')
        print('5. Logout')
        print("-"*50)
        
        option = input('Enter any option: ')

        if option == '1':
            role, username = login()
            if role == 'admin':
                admin_menu(username)
            else:
                print("Access denied. You are not an admin.")
        elif option == '2':
            role, username = login()
            if role == 'manager':
                manager_menu(username)
            else:
                print("Access denied. You are not a manager.")
        elif option == '3':
            role, username = login()
            if role == 'chef':
                chef_menu()
            else:
                print("Access denied. You are not a chef.")
        elif option == '4':
            role, username = login()
            if role == 'customer':
                customer_menu()
            else:
                print("Access denied. You are not a customer.")
        elif option == '5':
            print('Logged out successfully! Keep visiting')
            break
        else:
            print('Please select a valid option')

def main():
    decorate()
    menu()

if __name__ == "__main__":
    main()