import os
from datetime import datetime

# Define file paths
DATA_FOLDER = "data"
ORDER_FILE = os.path.join(DATA_FOLDER, "order.txt")
INGREDIENTS_FILE = os.path.join(DATA_FOLDER, "ingredients.txt")
USER_FILE = os.path.join(DATA_FOLDER, "user.txt")
SALES_FILE = os.path.join(DATA_FOLDER, "sales.txt")

# Ensure the data folder exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def chef_menu(username=None):
    """Main menu for chef interface"""
    while True:
        print(f"\nChef Menu (Logged in as: )")
        print("1. View Orders")
        print("2. Update Order Status")
        print("3. Request Ingredients")
        print("4. Update Profile")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_orders()
        elif choice == '2':
            update_order_status()
        elif choice == '3':
            request_ingredients()
        elif choice == '4':
            update_profile("chef", username)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

def view_orders():
    """Display all current orders"""
    print("\nCustomer Orders")
    if not os.path.exists(ORDER_FILE):
        print("No orders found.")
        return

    with open(ORDER_FILE, 'r') as file:
        for line in file:
            if not line.strip():
                continue

            parts = line.strip().split(',')
            if len(parts) == 5:
                order_id, item, quantity, price, status = parts
                print(f"Order ID: {order_id}, Item: {item}, Quantity: {quantity}, Price: ${price}, Status: {status}")
            else:
                print(f"Skipping invalid line: {line.strip()}")

def update_order_status():
    """Update the status of an order"""
    order_id = input("Enter order ID to update: ")
    status = input("Enter new status (In Progress/Completed): ").strip().title()

    if status not in ["In Progress", "Completed"]:
        print("Invalid status. Please enter 'In Progress' or 'Completed'.")
        return

    if not os.path.exists(ORDER_FILE):
        print("No orders found.")
        return

    with open(ORDER_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    with open(ORDER_FILE, 'w') as file:
        for line in lines:
            if not line.strip():
                continue

            parts = line.strip().split(',')
            if len(parts) == 5:
                current_order_id, item, quantity, price, current_status = parts
                if current_order_id == order_id:
                    found = True
                    if current_status == "Completed":
                        print(f"Cannot update order {order_id}. It is already {current_status}.")
                        file.write(line)
                    else:
                        file.write(f"{current_order_id},{item},{quantity},{price},{status}\n")
                        print("Order status updated successfully.")
                        if status == "Completed":
                            log_sale(current_order_id, item, quantity, price)
                else:
                    file.write(line)
            else:
                print(f"Skipping invalid line: {line.strip()}")

    if not found:
        print("Order not found.")

def log_sale(order_id, item, quantity, price):
    """Log a completed sale"""
    chef_name = "chef"  # This should ideally be the actual chef's username
    total_amount = float(quantity) * float(price)
    date = datetime.now().strftime("%Y-%m-%d")
    with open(SALES_FILE, 'a') as file:
        file.write(f"{order_id},{chef_name},{total_amount},{date},Completed\n")

def request_ingredients():
    """Request new ingredients"""
    ingredient = input("Enter the ingredient you need: ")
    with open(INGREDIENTS_FILE, 'a') as file:
        file.write(f"{ingredient}\n")
    print("Ingredient request submitted.")

def update_profile(role, current_user=None):
    """Update chef profile"""
    print(f"\nUpdate Chef Profile: {current_user}")
    print("(Leave blank to keep current value)\n")

    if not os.path.exists(USER_FILE):
        print("No user records found.")
        return

    with open(USER_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.strip() and len(line.strip().split(',')) >= 7:
            parts = line.strip().split(',')
            if parts[0] == current_user and parts[2] == "chef":
                found = True
                current_data = {
                    'line_index': i,
                    'username': parts[0],
                    'password': parts[1],
                    'role': parts[2],
                    'full_name': parts[3],
                    'contact': parts[4],
                    'address': parts[5],
                    'email': parts[6]
                }
                break

    if not found:
        print("Chef profile not found.")
        return

    # Get updated information with validation
    updated_data = current_data.copy()
    print('leave blank to keep current')
    # Password
    while True:
        new_password = input("New password (min 4 chars, leave blank to keep current): ").strip()
        if not new_password:
            break
        if len(new_password) >= 4:
            if new_password != current_data['password']:
                updated_data['password'] = new_password
                break
            print("New password must be different from current password.")
        else:
            print("Password must be at least 4 characters.")

    # Full Name
    while True:
        new_full_name = input(f"Full name : ").strip()
        if not new_full_name:
            break
        if new_full_name.replace(" ", "").isalpha():
            updated_data['full_name'] = new_full_name
            break
        print("Invalid name. Only letters and spaces allowed.")

    # Contact
    while True:
        new_contact = input(f"Contact : ").strip()
        if not new_contact:
            break
        if new_contact.isdigit() and len(new_contact) == 10:
            contact_exists = False
            for line in lines:
                if line.strip() and len(line.strip().split(',')) >= 5:
                    _, _, _, _, existing_contact, _, _ = line.strip().split(',', 5)
                    if existing_contact == new_contact and existing_contact != current_data['contact']:
                        contact_exists = True
                        break
            if not contact_exists:
                updated_data['contact'] = new_contact
                break
            print("Contact number already in use.")
        else:
            print("Contact must be 10 digits.")

    # Address
    new_address = input(f"Address [{current_data['address']}]: ").strip()
    if new_address:
        updated_data['address'] = new_address

    # Email
    while True:
        new_email = input(f"Email : ").strip()
        if not new_email:
            break
        if '@' in new_email and '.' in new_email.split('@')[-1]:
            email_exists = False
            for line in lines:
                if line.strip() and len(line.strip().split(',')) >= 7:
                    *_, existing_email = line.strip().rsplit(',', 1)
                    if existing_email == new_email and existing_email != current_data['email']:
                        email_exists = True
                        break
            if not email_exists:
                updated_data['email'] = new_email
                break
            print("Email already in use.")
        else:
            print("Invalid email format. Must contain @ and domain.")

    # Update the record
    lines[current_data['line_index']] = (
        f"{updated_data['username']},{updated_data['password']},chef,"
        f"{updated_data['full_name']},{updated_data['contact']},"
        f"{updated_data['address']},{updated_data['email']}\n"
    )

    with open(USER_FILE, 'w') as file:
        file.writelines(lines)
    
    print("\nChef profile updated successfully!")
    return updated_data['username']