import pymysql
from datetime import datetime

# Database connection function
def connect_db():
    try:
        con = pymysql.connect(
            host='localhost',
            user='root',
            password='shayan-khan321$',
            database='restaurant',
            port=3306
        )
        print("Database connection successful!")
        return con
    except Exception as e:
        print(f"Connection failed: {e}")
        exit()

# Function to show menu
def show_menu(cursor):
    cursor.execute("SELECT item_name, price FROM menu")
    rows = cursor.fetchall()
    print("\n--- Menu ---")
    for item, price in rows:
        print(f"{item}: {price} PKR")

# Function to create new customer
def create_customer(cursor, con):
    print("\n--- New Customer ---")
    name = input("Enter customer name: ").title()
    phone = int(input("Enter phone number: "))
    
    cursor.execute("INSERT INTO customers (customer_name, phone_number) VALUES (%s, %s)", 
                  (name, phone))
    con.commit()
    
    cursor.execute("SELECT LAST_INSERT_ID()")
    customer_id = cursor.fetchone()[0]
    print(f"Customer created! Your ID: {customer_id}")
    return customer_id

# Function to place order
# place_order function modify karein
def place_order(cursor, con, customer_id):
    show_menu(cursor)
    
    # Item ID se kaam karein
    try:
        item_id = int(input("\nEnter item ID: "))
    except:
        print("Please enter a valid item ID!")
        return
    
    # Pehle check karein item exists hai ya nahi
    cursor.execute("SELECT item_name, price FROM menu WHERE item_id=%s", (item_id,))
    result = cursor.fetchone()
    
    if not result:
        print("Item not found!")
        return
        
    item_name, price = result
    print(f"Selected item: {item_name} - {price} PKR")
    
    try:
        qty = int(input(f"Enter quantity for {item_name}: "))
    except:
        print("Please enter a valid number!")
        return
        
    total = price * qty
    
    # Ab item_id use karein
    cursor.execute("INSERT INTO orders (customer_id, item_id, qty, price) VALUES (%s, %s, %s, %s)", 
                  (customer_id, item_id, qty, total))
    con.commit()
    print(f"{qty} {item_name}(s) added to your order!")

# Function to view bill
def view_bill(cursor, customer_id):
    cursor.execute("""
        SELECT m.item_name, o.qty, o.price 
        FROM orders o
        JOIN menu m ON o.item_id = m.item_id
        WHERE o.customer_id = %s
    """, (customer_id,))
    
    rows = cursor.fetchall()
    
    if not rows:
        print("No orders yet!")
        return
        
    print(f"\n--- Bill for Customer ID: {customer_id} ---")
    total_bill = 0
    for item_name, qty, price in rows:
        print(f"{item_name} x {qty} = {price} PKR")
        total_bill += price
        
    print("-------------------")
    print(f"Total Amount: {total_bill} PKR")

# Function to remove item from order
def remove_item(cursor, con, customer_id):
    # Pehle customer ke orders dikhayein with item names
    cursor.execute("""
        SELECT m.item_name, o.qty 
        FROM orders o 
        JOIN menu m ON o.item_id = m.item_id 
        WHERE o.customer_id = %s
    """, (customer_id,))
    
    rows = cursor.fetchall()
    
    if not rows:
        print("No orders to remove!")
        return
        
    print("\n--- Your Orders ---")
    for item_name, qty in rows:
        print(f"{item_name} x {qty}")

    remove_item_name = input("\nEnter item name to remove: ").title()
    
    # Pehle item_name se item_id find karein
    cursor.execute("SELECT item_id FROM menu WHERE item_name = %s", (remove_item_name,))
    item_result = cursor.fetchone()
    
    if not item_result:
        print("Item not found in menu!")
        return
        
    item_id = item_result[0]
    
    # Ab orders table se check karein
    cursor.execute("SELECT qty FROM orders WHERE customer_id = %s AND item_id = %s", 
                  (customer_id, item_id))
    result = cursor.fetchone()
    
    if not result:
        print("Item not in your order!")
        return
        
    current_qty = result[0]
    try:
        remove_qty = int(input(f"Enter quantity to remove (Available: {current_qty}): "))
    except:
        print("Please enter a valid number!")
        return
        
    if remove_qty >= current_qty:
        # Complete item remove karein
        cursor.execute("DELETE FROM orders WHERE customer_id = %s AND item_id = %s", 
                      (customer_id, item_id))
        print(f"{remove_item_name} removed completely!")
    else:
        # Partial quantity remove karein
        new_qty = current_qty - remove_qty
        cursor.execute("UPDATE orders SET qty = %s WHERE customer_id = %s AND item_id = %s", 
                      (new_qty, customer_id, item_id))
        print(f"{remove_qty} {remove_item_name}(s) removed. Remaining: {new_qty}")
    
    con.commit()

# Main program
def main():
    con = connect_db()
    cursor = con.cursor()
    
    print("\n--- Restaurant Management System ---")
    print("1. New Customer")
    print("2. Existing Customer")
    choice = input("Enter choice (1-2): ")
    
    if choice == "1":
        customer_id = create_customer(cursor, con)
    elif choice == "2":
        try:
            customer_id = int(input("Enter your customer ID: "))
            # Verify customer exists
            cursor.execute("SELECT customer_id FROM customers WHERE customer_id=%s", (customer_id,))
            if not cursor.fetchone():
                print("Customer ID not found!")
                return
        except:
            print("Please enter a valid customer ID!")
            return
    else:
        print("Invalid choice!")
        return
    
    # Main menu loop
    while True:
        print(f"\nCustomer ID: {customer_id}")
        print("1. Show Menu")
        print("2. Place Order")
        print("3. View My Bill")
        print("4. Remove Item from Order")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            show_menu(cursor)
        elif choice == "2":
            place_order(cursor, con, customer_id)
        elif choice == "3":
            view_bill(cursor, customer_id)
        elif choice == "4":
            remove_item(cursor, con, customer_id)
        elif choice == "5":
            print("Thank you for visiting!")
            break
        else:
            print("Invalid choice! Please try again.")
    
    # Clean up
    cursor.close()
    con.close()

if __name__ == "__main__":
    main()