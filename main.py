menu = {
    "Burger": 350,
    "Pizza": 500,
    "Fries": 100,
    "Cold Drink": 100
}

order = {}

while True:
    print("\n--- Restaurant Management System ---")
    print("1. Show Menu")
    print("2. Place Order")
    print("3. View Bill")
    print("4. Exit")
    print("5. Remove Item from Order")   # New option

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\n--- Menu ---")
        for item, price in menu.items():
            print(f"{item} : {price} PKR")

    elif choice == "2":
        item = input("Enter the item you want to order: ").title()
        
        if item in menu:
            try:
                qty = int(input(f"Enter quantity for {item}: "))
            except ValueError:
                print("Please enter a valid number.")
                continue
            
            if item in order:
                order[item] += qty
            else:
                order[item] = qty

            print(f"{qty} {item}(s) added to your order.")
        else:
            print("Sorry, this item is not available.")

    elif choice == "3":
        if not order:   
            print("You have not ordered anything yet.")
        else:
            print("\n--- Your Bill ---")
            total = 0
            for item, qty in order.items():
                price = menu[item] * qty
                print(f"{item} x {qty} = {price} PKR")
                total += price
            print(f"Total Bill = {total} PKR")

    elif choice == "4":
        print("Exiting... Thank you!")
        break

    elif choice == "5":   # Remove item logic
        if not order:
            print("Your order is empty. Nothing to remove.")
        else:
            print("\n--- Current Order ---")
            for item, qty in order.items():
                print(f"{item} x {qty}")
            
            remove_item = input("Enter the item you want to remove: ")

            if remove_item in order:
                try:
                    remove_qty = int(input(f"Enter quantity to remove for {remove_item}: "))
                except ValueError:
                    print("Please enter a valid number.")
                    continue

                if remove_qty >= order[remove_item]:
                    del order[remove_item]
                    print(f"{remove_item} removed from your order.")
                else:
                    order[remove_item] -= remove_qty
                    print(f"{remove_qty} {remove_item}(s) removed. Remaining: {order[remove_item]}")
            else:
                print("Item not found in your order.")

    else:
        print("Invalid choice. Please try again.")
