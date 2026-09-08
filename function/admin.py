import os
from datetime import datetime

# Define file paths
DATA_FOLDER = "data"
USER_FILE = os.path.join(DATA_FOLDER, "user.txt")
FEEDBACK_FILE = os.path.join(DATA_FOLDER, "feedback.txt")
SALES_FILE = os.path.join(DATA_FOLDER, "sales.txt")

# Ensure the data folder exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def admin_menu(current_admin):
    while True:
        print("\nAdmin Menu")
        print("1. Manage Staff")
        print("2. View Sales Report")
        print("3. View Customer Feedback")
        print("4. Update My Profile")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            manage_staff()
        elif choice == '2':
            view_sales_report()
        elif choice == '3':
            view_feedback()
        elif choice == '4':
            update_profile(current_admin)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def manage_staff():
    while True:
        print("\nManage Staff")
        print("1. Add Staff")
        print("2. Edit Staff")
        print("3. Delete Staff")
        print("4. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_staff()
        elif choice == '2':
            edit_staff()
        elif choice == '3':
            delete_staff()
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")

def add_staff():
    print("\nAdd New Staff (Manager/Chef)")
    
    # Validate username
    while True:
        username = input("Enter new staff username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
            
        # Check if username exists
        username_exists = False
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) > 0 and parts[0] == username:
                        username_exists = True
                        break
        if username_exists:
            print("Username already exists. Please choose another.")
        else:
            break

    # Validate password
    while True:
        password = input("Enter new staff password: ").strip()
        if len(password) >= 4:
            break
        print("Password must be at least 4 characters.")

    # Validate staff role
    while True:
        role = input("Enter staff role (manager/chef): ").strip().lower()
        if role in ["manager", "chef"]:
            break
        print("Invalid role. Only 'manager' or 'chef' allowed.")

    # Validate full name
    while True:
        full_name = input("Enter staff full name: ").strip()
        if full_name and all(x.isalpha() or x.isspace() for x in full_name):
            break
        print("Invalid name. Only letters and spaces allowed.")

    # Validate contact number
    while True:
        contact = input("Enter staff contact number (10 digits): ").strip()
        if contact.isdigit() and len(contact) == 10:
            # Check if contact exists
            contact_exists = False
            if os.path.exists(USER_FILE):
                with open(USER_FILE, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')
                        if len(parts) > 4 and parts[4] == contact:
                            contact_exists = True
                            break
            if not contact_exists:
                break
            print("Contact number already in use.")
        else:
            print("Contact must be 10 digits.")

    # Validate address
    while True:
        address = input("Enter staff address: ").strip()
        if address:
            break
        print("Address cannot be empty.")

    # Validate email
    while True:
        email = input("Enter staff email (must contain @ and domain): ").strip()
        if '@' in email and '.' in email.split('@')[-1]:
            # Check if email exists
            email_exists = False
            if os.path.exists(USER_FILE):
                with open(USER_FILE, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')
                        if len(parts) > 6 and parts[6] == email:
                            email_exists = True
                            break
            if not email_exists:
                break
            print("Email already in use.")
        else:
            print("Invalid email format. Must contain @ and domain.")

    # Add the new staff member
    with open(USER_FILE, 'a') as file:
        file.write(f"{username},{password},{role},{full_name},{contact},{address},{email}\n")
    print(f"\nStaff {username} added successfully as {role}.")

def edit_staff():
    username = input("\nEnter staff username to edit: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    if not os.path.exists(USER_FILE):
        print("No staff records found.")
        return

    with open(USER_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    for i, line in enumerate(lines):
        if not line.strip() or len(line.strip().split(',')) != 7:
            continue
            
        uname, pwd, role, fname, cnt, addr, eml = line.strip().split(',')
        if uname == username:
            if role == 'admin':
                print("Cannot edit another admin account.")
                return
            found = True
            break

    if not found:
        print("Staff not found.")
        return

    print(f"\nEditing staff: {username} (Current role: {role})")
    print("Leave fields blank to keep current values\n")

    # Get updated information with validation
    updated_data = {
        'username': uname,
        'password': pwd,
        'role': role,
        'full_name': fname,
        'contact': cnt,
        'address': addr,
        'email': eml
    }

    # Password
    while True:
        new_password = input("New password (leave blank to keep current): ").strip()
        if not new_password:
            break
        if len(new_password) >= 4:
            if new_password != pwd:
                updated_data['password'] = new_password
                break
            print("New password must be different from current password.")
        else:
            print("Password must be at least 4 characters.")

    # Role (only allow changing between manager and chef)
    while True:
        new_role = input(f"New role (manager/chef) : ").strip().lower()
        if not new_role:
            break
        if new_role in ['manager', 'chef']:
            updated_data['role'] = new_role
            break
        print("Invalid role. Only 'manager' or 'chef' allowed.")

    # Full Name
    while True:
        new_full_name = input(f"New full name : ").strip()
        if not new_full_name:
            break
        if new_full_name.replace(" ", "").isalpha():
            updated_data['full_name'] = new_full_name
            break
        print("Invalid name. Only letters and spaces allowed.")

    # Contact
    while True:
        new_contact = input(f"New contact number : ").strip()
        if not new_contact:
            break
        if new_contact.isdigit() and len(new_contact) == 10:
            # Check if contact exists in other records
            contact_exists = False
            for line in lines:
                if line.strip() and len(line.strip().split(',')) >= 5:
                    _, _, _, _, existing_contact, _, _ = line.strip().split(',', 5)
                    if existing_contact == new_contact and existing_contact != cnt:
                        contact_exists = True
                        break
            if not contact_exists:
                updated_data['contact'] = new_contact
                break
            print("Contact number already in use.")
        else:
            print("Contact must be 10 digits.")

    # Address
    new_address = input(f"New address : ").strip()
    if new_address:
        updated_data['address'] = new_address

    # Email
    while True:
        new_email = input(f"New email : ").strip()
        if not new_email:
            break
        if '@' in new_email and '.' in new_email.split('@')[-1]:
            # Check if email exists in other records
            email_exists = False
            for line in lines:
                if line.strip() and len(line.strip().split(',')) >= 7:
                    *_, existing_email = line.strip().rsplit(',', 1)
                    if existing_email == new_email and existing_email != eml:
                        email_exists = True
                        break
            if not email_exists:
                updated_data['email'] = new_email
                break
            print("Email already in use.")
        else:
            print("Invalid email format. Must contain @ and domain.")

    # Update the line
    lines[i] = f"{updated_data['username']},{updated_data['password']},{updated_data['role']}," \
               f"{updated_data['full_name']},{updated_data['contact']}," \
               f"{updated_data['address']},{updated_data['email']}\n"

    with open(USER_FILE, 'w') as file:
        file.writelines(lines)
    
    print(f"\nStaff {username} updated successfully!")

def delete_staff():
    username = input("\nEnter staff username to delete: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    if not os.path.exists(USER_FILE):
        print("No staff records found.")
        return

    with open(USER_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    with open(USER_FILE, 'w') as file:
        for line in lines:
            if not line.strip() or len(line.strip().split(',')) != 7:
                file.write(line)
                continue

            uname, pwd, role, fname, cnt, addr, eml = line.strip().split(',')
            if uname == username:
                if role == 'customer':
                    print("Cannot delete customer accounts from staff management.")
                    file.write(line)  # Keep the customer record
                elif role == 'admin':
                    print("Cannot delete admin accounts.")
                    file.write(line)  # Keep the admin record
                else:
                    found = True
                    print(f"Staff {username} deleted successfully.")
            else:
                file.write(line)

    if not found:
        print("Staff not found or cannot be deleted.")

def view_sales_report():
    while True:
        print("\nSales Report Menu")
        print("1. View Sales by Month")
        print("2. View Sales by Chef")
        print("3. View All Sales")
        print("4. Back")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_sales_by_month()
        elif choice == '2':
            view_sales_by_chef()
        elif choice == '3':
            view_all_sales()
        elif choice == '4':
            return
        else:
            print("Invalid choice. Please try again.")

def view_sales_by_month():
    while True:
        month = input("\nEnter the month (1-12): ").strip()
        if month.isdigit() and 1 <= int(month) <= 12:
            break
        print("Invalid month. Must be between 1-12.")

    while True:
        year = input("Enter the year (e.g., 2023): ").strip()
        if year.isdigit() and len(year) == 4:
            break
        print("Invalid year. Must be 4 digits.")

    if not os.path.exists(SALES_FILE):
        print("No sales data found.")
        return

    total_sales = 0
    print(f"\nSales for {month}/{year}:")
    print("-" * 70)
    print("{:<10} {:<15} {:<10} {:<15} {:<10}".format(
        "Order ID", "Chef", "Amount", "Date", "Status"))
    print("-" * 70)

    with open(SALES_FILE, 'r') as file:
        for line in file:
            if not line.strip():
                continue

            parts = line.strip().split(',')
            if len(parts) == 5:
                order_id, chef_name, total_amount, date, status = parts
                try:
                    order_date = datetime.strptime(date, "%Y-%m-%d")
                    if order_date.month == int(month) and order_date.year == int(year):
                        total_sales += float(total_amount)
                        print("{:<10} {:<15} ${:<9.2f} {:<15} {:<10}".format(
                            order_id, chef_name, float(total_amount), date, status))
                except ValueError:
                    continue

    print("-" * 70)
    print(f"\nTotal Sales for {month}/{year}: ${total_sales:.2f}")

def view_sales_by_chef():
    chef_name = input("\nEnter the chef's username: ").strip()
    if not chef_name:
        print("Chef username cannot be empty.")
        return

    if not os.path.exists(SALES_FILE):
        print("No sales data found.")
        return

    total_sales = 0
    print(f"\nSales by Chef {chef_name}:")
    print("-" * 70)
    print("{:<10} {:<10} {:<15} {:<10}".format(
        "Order ID", "Amount", "Date", "Status"))
    print("-" * 70)

    with open(SALES_FILE, 'r') as file:
        for line in file:
            if not line.strip():
                continue

            parts = line.strip().split(',')
            if len(parts) == 5:
                order_id, chef, total_amount, date_time, status = parts
                if chef == chef_name:
                    total_sales += float(total_amount)
                    print("{:<10} ${:<9.2f} {:<15} {:<10}".format(
                        order_id, float(total_amount), date_time, status))

    print("-" * 70)
    print(f"\nTotal Sales by Chef {chef_name}: ${total_sales:.2f}")

def view_all_sales():
    if not os.path.exists(SALES_FILE):
        print("No sales data found.")
        return

    total_sales = 0
    print("\nAll Sales Records:")
    print("-" * 85)
    print("{:<10} {:<15} {:<10} {:<15} {:<15} {:<10}".format(
        "Order ID", "Chef", "Amount", "Date", "Time", "Status"))
    print("-" * 85)

    with open(SALES_FILE, 'r') as file:
        for line in file:
            if not line.strip():
                continue

            parts = line.strip().split(',')
            if len(parts) == 5:
                order_id, chef_name, total_amount, date_time, status = parts
                try:
                    # Split date and time if they're combined
                    if ' ' in date_time:
                        date, time = date_time.split(' ')
                    else:
                        date = date_time
                        time = "00:00"
                    total_sales += float(total_amount)
                    print("{:<10} {:<15} ${:<9.2f} {:<15} {:<15} {:<10}".format(
                        order_id, chef_name, float(total_amount), date, time, status))
                except ValueError:
                    continue

    print("-" * 85)
    print(f"\nTotal Sales: ${total_sales:.2f}")

def view_feedback():
    print("\nCustomer Feedback")
    if not os.path.exists(FEEDBACK_FILE):
        print("No feedback found.")
        return

    print("-" * 100)
    print("{:<15} {:<30} {:<50}".format("Customer", "Subject", "Message"))
    print("-" * 100)

    with open(FEEDBACK_FILE, 'r') as file:
        for line in file:
            if line.strip() and len(line.strip().split(',')) == 3:
                customer, subject, message = line.strip().split(',', 2)
                print("{:<15} {:<30} {:<50}".format(
                    customer, subject, message[:47] + "..." if len(message) > 50 else message))

def update_profile(current_admin):
    print(f"\nUpdate Admin Profile: {current_admin}")
    print("(Leave blank to keep current value)\n")

    if not os.path.exists(USER_FILE):
        print("Error: User database not found!")
        return current_admin

    # Read all user records
    with open(USER_FILE, 'r') as file:
        lines = file.readlines()

    # Find admin record
    admin_record = None
    for i, line in enumerate(lines):
        if line.strip():
            parts = line.strip().split(',')
            if len(parts) >= 7 and parts[0] == current_admin and parts[2] == 'admin':
                admin_record = {
                    'index': i,
                    'username': parts[0],
                    'password': parts[1],
                    'role': parts[2],
                    'full_name': parts[3],
                    'contact': parts[4],
                    'address': parts[5],
                    'email': parts[6]
                }
                break

    if not admin_record:
        print("Error: Admin profile not found in database!")
        return current_admin

    # Get updates with retry for invalid inputs
    def get_valid_input(prompt, current_value, validation_func, error_msg):
        while True:
            new_value = input(prompt).strip()
            if not new_value:
                return current_value
            if validation_func(new_value):
                return new_value
            print(error_msg)
            print("Please try again or leave blank to keep current value")

    # Username
    def validate_username(username):
        if username == admin_record['username']:
            return True
        return not any(
            line.split(',')[0] == username 
            for line in lines 
            if line.strip()
        )
    
    new_username = get_valid_input(
        f"New username: ",
        admin_record['username'],
        validate_username,
        "Username already taken!"
    )

    # Password
    new_password = get_valid_input(
        "New password (min 4 chars): ",
        admin_record['password'],
        lambda p: len(p) >= 4,
        "Password must be at least 4 characters"
    )

    # Full Name
    new_name = get_valid_input(
        f"Full name : ",
        admin_record['full_name'],
        lambda n: n.replace(" ", "").isalpha(),
        "Name can only contain letters and spaces"
    )

    # Contact
    new_contact = get_valid_input(
        f"Contact : ",
        admin_record['contact'],
        lambda c: c.isdigit() and len(c) == 10 and not any(
            len(line.split(',')) > 4 and line.split(',')[4] == c
            for line in lines
            if line.strip() and line.split(',')[0] != current_admin
        ),
        "Must be 10 unique digits"
    )

    # Address
    new_address = input(f"Address : ").strip() or admin_record['address']

    # Email
    new_email = get_valid_input(
        f"Email : ",
        admin_record['email'],
        lambda e: '@' in e and '.' in e.split('@')[-1] and not any(
            len(line.split(',')) > 6 and line.split(',')[6] == e
            for line in lines
            if line.strip() and line.split(',')[0] != current_admin
        ),
        "Invalid email format or already in use"
    )

    # Update the record
    updated_record = f"{new_username},{new_password},admin,{new_name},{new_contact},{new_address},{new_email}\n"
    lines[admin_record['index']] = updated_record

    # Write back to file
    with open(USER_FILE, 'w') as file:
        file.writelines(lines)

    print("\nProfile updated successfully!")
    return new_username