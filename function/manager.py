import os

# File paths
DATA_FOLDER = "data"
USER_FILE = os.path.join(DATA_FOLDER, "user.txt")
MENU_FILE = os.path.join(DATA_FOLDER, "menu.txt")
INGREDIENTS_FILE = os.path.join(DATA_FOLDER, "ingredients.txt")

def manager_menu(current_manager):
    while True:
        print("\nManager Menu")
        print("1. Manage Customers")
        print("2. Manage Menu")
        print("3. View Ingredients List")
        print("4. Update Profile")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            manage_customers()
        elif choice == '2':
            manage_menu()
        elif choice == '3':
            view_ingredients()
        elif choice == '4':
            current_manager = update_profile(current_manager, "manager")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def manage_customers():
    while True:
        print("\nManage Customers")
        print("1. Add Customer")
        print("2. Edit Customer")
        print("3. Delete Customer")
        print("4. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_customer()
        elif choice == '2':
            edit_customer()
        elif choice == '3':
            delete_customer()
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")

def add_customer():
    print("\nAdd New Customer")
    
    # Username validation
    while True:
        username = input("Username: ").strip()
        if not username:
            print("Username cannot be empty")
            continue
            
        # Check if username exists
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r') as file:
                for line in file:
                    if line.strip() and line.split(',')[0] == username:
                        print("Username already exists")
                        break
                else:
                    break
        else:
            break

    # Password validation
    while True:
        password = input("Password (min 4 chars): ").strip()
        if len(password) >= 4:
            break
        print("Password too short")

    # Name validation
    while True:
        name = input("Full Name: ").strip()
        if name and name.replace(" ", "").isalpha():
            break
        print("Invalid name")

    # Contact validation
    while True:
        contact = input("Contact (10 digits): ").strip()
        if contact.isdigit() and len(contact) == 10:
            # Check if contact exists
            if os.path.exists(USER_FILE):
                with open(USER_FILE, 'r') as file:
                    for line in file:
                        if line.strip() and len(line.split(',')) > 4 and line.split(',')[4] == contact:
                            print("Contact already in use")
                            break
                    else:
                        break
            else:
                break
        else:
            print("Invalid contact")

    # Address
    address = input("Address: ").strip()
    while not address:
        print("Address cannot be empty")
        address = input("Address: ").strip()

    # Email validation
    while True:
        email = input("Email: ").strip()
        if '@' in email and '.' in email.split('@')[-1]:
            # Check if email exists
            if os.path.exists(USER_FILE):
                with open(USER_FILE, 'r') as file:
                    for line in file:
                        if line.strip() and len(line.split(',')) > 6 and line.split(',')[6] == email:
                            print("Email already in use")
                            break
                    else:
                        break
            else:
                break
        else:
            print("Invalid email")

    # Save customer
    with open(USER_FILE, 'a') as file:
        file.write(f"{username},{password},customer,{name},{contact},{address},{email}\n")
    print("Customer added successfully")

def edit_customer():
    username = input("\nEnter customer username to edit: ").strip()
    if not username:
        print("Username cannot be empty")
        return

    if not os.path.exists(USER_FILE):
        print("No customers found")
        return

    with open(USER_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.strip() and len(line.split(',')) == 7:
            parts = line.strip().split(',')
            if parts[0] == username and parts[2] == 'customer':
                found = True
                break

    if not found:
        print("Customer not found")
        return

    print(f"\nEditing customer: {username}")
    current_data = parts

    # Get updates
    new_password = input("New password (leave blank to keep current): ").strip()
    if new_password:
        if len(new_password) >= 4:
            if new_password != current_data[1]:
                current_data[1] = new_password
            else:
                print("New password must be different")
        else:
            print("Password too short")

    new_name = input("Full name (leave blank to keep current): ").strip()
    if new_name and new_name.replace(" ", "").isalpha():
        current_data[3] = new_name

    new_contact = input("Contact (leave blank to keep current): ").strip()
    if new_contact:
        if new_contact.isdigit() and len(new_contact) == 10:
            # Check contact uniqueness
            contact_unique = True
            for line in lines:
                if line.strip() and len(line.split(',')) > 4:
                    if line.split(',')[4] == new_contact and line.split(',')[0] != username:
                        contact_unique = False
                        break
            if contact_unique:
                current_data[4] = new_contact
            else:
                print("Contact already in use")
        else:
            print("Invalid contact")

    new_address = input("Address (leave blank to keep current): ").strip()
    if new_address:
        current_data[5] = new_address

    new_email = input("Email (leave blank to keep current): ").strip()
    if new_email:
        if '@' in new_email and '.' in new_email.split('@')[-1]:
            # Check email uniqueness
            email_unique = True
            for line in lines:
                if line.strip() and len(line.split(',')) > 6:
                    if line.split(',')[6] == new_email and line.split(',')[0] != username:
                        email_unique = False
                        break
            if email_unique:
                current_data[6] = new_email
            else:
                print("Email already in use")
        else:
            print("Invalid email")

    # Update record
    lines[i] = ','.join(current_data) + '\n'

    # Save changes
    with open(USER_FILE, 'w') as file:
        file.writelines(lines)
    print("Customer updated successfully")

def delete_customer():
    username = input("\nEnter customer username to delete: ").strip()
    if not username:
        print("Username cannot be empty")
        return

    if not os.path.exists(USER_FILE):
        print("No customers found")
        return

    with open(USER_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    with open(USER_FILE, 'w') as file:
        for line in lines:
            if line.strip() and len(line.split(',')) == 7:
                parts = line.strip().split(',')
                if parts[0] == username and parts[2] == 'customer':
                    found = True
                    continue
            file.write(line)

    if found:
        print("Customer deleted successfully")
    else:
        print("Customer not found")

def manage_menu():
    while True:
        print("\nManage Menu")
        print("1. Add Menu Item")
        print("2. Edit Menu Item")
        print("3. Delete Menu Item")
        print("4. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_menu_item()
        elif choice == '2':
            edit_menu_item()
        elif choice == '3':
            delete_menu_item()
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")

def add_menu_item():
    name = input("Enter menu item name: ")
    category = input("Enter menu item category: ")
    price = input("Enter menu item price: ")

    # Check if the menu item already exists
    if os.path.exists(MENU_FILE):
        with open(MENU_FILE, 'r') as file:
            for line in file:
                if not line.strip() or len(line.strip().split(',')) != 3:
                    continue
                item_name, _, _ = line.strip().split(',')
                if item_name.lower() == name.lower():
                    print("Menu item with this name already exists")
                    return

    # Add the new menu item
    with open(MENU_FILE, 'a') as file:
        file.write(f"{name},{category},{price}\n")
    print("Menu item added successfully")

def edit_menu_item():
    name = input("Enter menu item name to edit: ")
    new_name = input("Enter new name (leave blank to keep current): ").strip()
    new_category = input("Enter new category (leave blank to keep current): ").strip()
    new_price = input("Enter new price (leave blank to keep current): ").strip()

    if not os.path.exists(MENU_FILE):
        print("No menu items found")
        return

    with open(MENU_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    with open(MENU_FILE, 'w') as file:
        for line in lines:
            if not line.strip() or len(line.strip().split(',')) != 3:
                file.write(line)
                continue

            item_name, category, price = line.strip().split(',')
            if item_name.lower() == name.lower():
                found = True

                # Check if new name is provided and unique
                if new_name:
                    for check_line in lines:
                        check_item_name, _, _ = check_line.strip().split(',')
                        if check_item_name.lower() == new_name.lower():
                            print("Menu item with this name already exists")
                            file.write(line)  # Keep the original line
                            return
                    item_name = new_name  # Update name

                # Check if new category is provided
                if new_category:
                    category = new_category  # Update category

                # Check if new price is provided
                if new_price:
                    price = new_price  # Update price

                # Write the updated line
                file.write(f"{item_name},{category},{price}\n")
                print("Menu item updated successfully")
            else:
                file.write(line)

    if not found:
        print("Menu item not found")

def delete_menu_item():
    name = input("Enter menu item name to delete: ")

    if not os.path.exists(MENU_FILE):
        print("No menu items found")
        return

    with open(MENU_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    with open(MENU_FILE, 'w') as file:
        for line in lines:
            if not line.strip() or len(line.strip().split(',')) != 3:
                file.write(line)
                continue

            item_name, _, _ = line.strip().split(',')
            if item_name.lower() == name.lower():
                found = True
            else:
                file.write(line)

    if found:
        print("Menu item deleted successfully")
    else:
        print("Menu item not found")

def view_ingredients():
    print("\nIngredients List")
    if not os.path.exists(INGREDIENTS_FILE):
        print("No ingredients found")
        return

    with open(INGREDIENTS_FILE, 'r') as file:
        for line in file:
            print(line.strip())

def update_profile(current_user, role):
    print(f"\nUpdate Profile: {current_user}")
    
    if not os.path.exists(USER_FILE):
        print("No users found")
        return current_user

    with open(USER_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.strip() and len(line.split(',')) == 7:
            parts = line.strip().split(',')
            if parts[0] == current_user and parts[2] == role:
                found = True
                break

    if not found:
        print("User not found")
        return current_user

    print("Leave blank to keep current value")
    current_data = parts

    # Password
    new_password = input("New password (min 4 chars): ").strip()
    if new_password:
        if len(new_password) >= 4:
            if new_password != current_data[1]:
                current_data[1] = new_password
            else:
                print("New password must be different")
        else:
            print("Password too short")

    # Name
    new_name = input("Full name: ").strip()
    if new_name and new_name.replace(" ", "").isalpha():
        current_data[3] = new_name

    # Contact
    new_contact = input("Contact (10 digits): ").strip()
    if new_contact:
        if new_contact.isdigit() and len(new_contact) == 10:
            # Check contact uniqueness
            contact_unique = True
            for line in lines:
                if line.strip() and len(line.split(',')) > 4:
                    if line.split(',')[4] == new_contact and line.split(',')[0] != current_user:
                        contact_unique = False
                        break
            if contact_unique:
                current_data[4] = new_contact
            else:
                print("Contact already in use")
        else:
            print("Invalid contact")

    # Address
    new_address = input("Address: ").strip()
    if new_address:
        current_data[5] = new_address

    # Email
    new_email = input("Email: ").strip()
    if new_email:
        if '@' in new_email and '.' in new_email.split('@')[-1]:
            # Check email uniqueness
            email_unique = True
            for line in lines:
                if line.strip() and len(line.split(',')) > 6:
                    if line.split(',')[6] == new_email and line.split(',')[0] != current_user:
                        email_unique = False
                        break
            if email_unique:
                current_data[6] = new_email
            else:
                print("Email already in use")
        else:
            print("Invalid email")

    # Update record
    lines[i] = ','.join(current_data) + '\n'

    # Save changes
    with open(USER_FILE, 'w') as file:
        file.writelines(lines)
    print("Profile updated successfully")
    return current_data[0]  # Return username in case it was changed

def is_admin(username):
    """Check if user is admin"""
    if not os.path.exists(USER_FILE):
        return False

    with open(USER_FILE, 'r') as file:
        for line in file:
            if line.strip() and len(line.strip().split(',')) >= 3:
                parts = line.strip().split(',')
                if parts[0] == username and parts[2] == 'admin':
                    return True
    return False