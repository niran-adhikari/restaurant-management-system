import os
from datetime import datetime

# Define file paths
DATA_FOLDER = "data"
MENU_FILE = os.path.join(DATA_FOLDER, "menu.txt")
ORDER_FILE = os.path.join(DATA_FOLDER, "order.txt")
FEEDBACK_FILE = os.path.join(DATA_FOLDER, "feedback.txt")
USER_FILE = os.path.join(DATA_FOLDER, "user.txt")
SALES_FILE = os.path.join(DATA_FOLDER, "sales.txt")

# Ensure the data folder exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

def customer_menu():
    while True:
        print("\nCustomer Menu")
        print("1. View Menu")
        print("2. Place Order")
        print("3. View Order Status")
        print("4. Edit Order")
        print("5. Delete Order")
        print("6. Pay to Confirm Order")
        print("7. Send Feedback")
        print("8. Update Profile")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            view_menu()
        elif choice == '2':
            place_order()
        elif choice == '3':
            view_order_status()
        elif choice == '4':
            edit_order()
        elif choice == '5':
            delete_order()
        elif choice == '6':
            pay_to_confirm()
        elif choice == '7':
            send_feedback()
        elif choice == '8':
            update_profile("customer")
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please try again.")

def view_menu():
    print("\nRestaurant Menu")
    if not os.path.exists(MENU_FILE):
        print("Menu file not found.")
        return

    with open(MENU_FILE, 'r') as file:
        for line in file:
            if not line.strip() or len(line.strip().split(',')) != 3:
                continue
            item_name, category, price = line.strip().split(',')
            print(f"{item_name} ({category}): ${price}")

def place_order():
    print("\nPlace Order")
    view_menu()  # Show the menu to the customer

    orders = []
    while True:
        item = input("Enter the item name to order (or type 'done' to finish): ").strip()
        if item.lower() == 'done':
            break

        quantity = input("Enter the quantity: ").strip()

        # Check if the item exists in the menu
        if not os.path.exists(MENU_FILE):
            print("Menu file not found.")
            return

        with open(MENU_FILE, 'r') as file:
            menu_items = [line.strip().split(',')[0].lower() for line in file if line.strip()]

        if item.lower() not in menu_items:
            print("Item not found in the menu. Please try again.")
            continue

        # Get the price of the item
        with open(MENU_FILE, 'r') as file:
            for line in file:
                if not line.strip():
                    continue
                item_name, category, price = line.strip().split(',')
                if item_name.lower() == item.lower():
                    orders.append((item, int(quantity), float(price)))
                    break

    if not orders:
        print("No items added to the order.")
        return

    # Calculate the total amount
    total_amount = sum(quantity * price for item, quantity, price in orders)

    # Display the order summary
    print("\nOrder Summary:")
    for item, quantity, price in orders:
        print(f"{item} x {quantity} = ${quantity * price}")
    print(f"Total Amount: ${total_amount}")

    # Generate a unique Order ID
    new_order_id = 1  # Default Order ID if no orders exist
    if os.path.exists(ORDER_FILE):
        with open(ORDER_FILE, 'r') as file:
            existing_orders = file.readlines()
            if existing_orders:
                # Find the last valid Order ID
                for line in reversed(existing_orders):
                    try:
                        last_order_id = int(line.strip().split(',')[0])
                        new_order_id = last_order_id + 1
                        break
                    except (ValueError, IndexError):
                        continue  # Skip invalid lines

    # Save the order to the order file
    with open(ORDER_FILE, 'a') as file:
        for item, quantity, price in orders:
            file.write(f"{new_order_id},{item},{quantity},{price},Pending\n")
    print(f"Order placed successfully. Your Order ID is: {new_order_id}")

def view_order_status():
    print("\nOrder Status")
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

def edit_order():
    print("\nEdit Order")
    view_order_status()  # Show the current orders
    order_id = input("Enter the Order ID to edit: ").strip()
    new_item = input("Enter the new item name (leave blank to keep current): ").strip()
    new_quantity = input("Enter the new quantity (leave blank to keep current): ").strip()

    if not os.path.exists(ORDER_FILE):
        print("No orders found.")
        return

    with open(ORDER_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    with open(ORDER_FILE, 'w') as file:
        for line in lines:
            if line.startswith(order_id + ","):
                found = True
                order_id, item, quantity, price, status = line.strip().split(',')
                if new_item:
                    item = new_item
                if new_quantity:
                    quantity = new_quantity
                file.write(f"{order_id},{item},{quantity},{price},{status}\n")
            else:
                file.write(line)

    if found:
        print("Order updated successfully.")
    else:
        print("Order not found.")

def delete_order():
    print("\nDelete Order")
    view_order_status()  # Show the current orders
    order_id = input("Enter the Order ID to delete: ").strip()

    if not os.path.exists(ORDER_FILE):
        print("No orders found.")
        return

    with open(ORDER_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    with open(ORDER_FILE, 'w') as file:
        for line in lines:
            if not line.startswith(order_id + ","):
                file.write(line)
            else:
                found = True

    if found:
        print("Order deleted successfully.")
    else:
        print("Order not found.")

def pay_to_confirm():
    print("\nPay to Confirm")
    view_order_status()  # Show the current orders
    order_id = input("Enter the Order ID to confirm payment: ").strip()

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

                    # Allow payment for orders that are Pending or In Progress
                    if current_status in ["Pending", "In Progress"]:
                        file.write(f"{current_order_id},{item},{quantity},{price},Paid\n")
                        print("Payment confirmed. Order marked as Paid.")

                        # Log the sale when payment is confirmed
                        log_sale(current_order_id, item, quantity, price)
                    else:
                        print(f"Cannot pay for order {order_id}. It is already {current_status}.")
                        file.write(line)  # Keep the original line
                else:
                    file.write(line)  # Keep the original line
            else:
                print(f"Skipping invalid line: {line.strip()}")

    if not found:
        print("Order not found.")

def log_sale(order_id, item, quantity, price):
    chef_name = "chef_c"  # Replace with the actual chef's username (you can pass this as a parameter)
    total_amount = float(quantity) * float(price)
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time

    # Log the sale to the SALES_FILE
    with open(SALES_FILE, 'a') as file:
        file.write(f"{order_id},{chef_name},{total_amount},{date_time},Paid\n")
    print(f"Sale logged for Order ID {order_id} on {date_time}.")


def send_feedback():
    feedback = input("Enter your feedback: ")
    with open(FEEDBACK_FILE, 'a') as file:
        file.write(f"{feedback}\n")
    print("Feedback sent successfully.")

def update_profile(role, current_user=None, current_user_role=None):
    """
    Update profile for customer (modified to work without parameters)
    """
    if role != "customer":
        print("Access denied. Only customer profiles can be updated here.")
        return

    print("\nUpdate Your Profile")
    print("(Leave blank to keep current value)\n")

    # Get the current username (you'll need to modify main.py slightly)
    # For now, we'll ask for username to maintain functionality
    username = input("Enter your username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    if not os.path.exists(USER_FILE):
        print("No user records found.")
        return

    # Read all records and find the customer profile
    with open(USER_FILE, 'r') as file:
        lines = file.readlines()

    found = False
    current_data = None
    for i, line in enumerate(lines):
        if line.strip() and len(line.strip().split(',')) >= 7:
            parts = line.strip().split(',')
            if parts[0] == username and parts[2] == "customer":
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
        print("Customer profile not found.")
        return

    # Get updated information with validation
    updated_data = current_data.copy()

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
        new_full_name = input(f"Full name [{current_data['full_name']}]: ").strip()
        if not new_full_name:
            break
        if new_full_name.replace(" ", "").isalpha():
            updated_data['full_name'] = new_full_name
            break
        print("Invalid name. Only letters and spaces allowed.")

    # Contact
    while True:
        new_contact = input(f"Contact [{current_data['contact']}]: ").strip()
        if not new_contact:
            break
        if new_contact.isdigit() and len(new_contact) == 10:
            # Check contact uniqueness
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
        new_email = input(f"Email [{current_data['email']}]: ").strip()
        if not new_email:
            break
        if '@' in new_email and '.' in new_email.split('@')[-1]:
            # Check email uniqueness
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
        f"{updated_data['username']},{updated_data['password']},customer,"
        f"{updated_data['full_name']},{updated_data['contact']},"
        f"{updated_data['address']},{updated_data['email']}\n"
    )

    with open(USER_FILE, 'w') as file:
        file.writelines(lines)
    
    print("\nCustomer profile updated successfully!")
    return updated_data['username']
