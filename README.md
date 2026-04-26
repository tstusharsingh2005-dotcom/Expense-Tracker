import os

FILE_NAME = "expenses.txt"

categories = ["Food", "Travel", "Shopping", "Bills", "Other"]

def add_expense():
    date = input("Enter date (DD-MM-YYYY): ")
    
    print("\nSelect Category:")
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")
    
    choice = int(input("Enter category number: "))
    
    if choice < 1 or choice > len(categories):
        print("Invalid category!\n")
        return
    
    category = categories[choice - 1]
    amount = float(input("Enter amount: "))

    with open(FILE_NAME, "a") as file:
        file.write(f"{date},{category},{amount}\n")

    print("Expense added successfully!\n")


def view_expense():
    if not os.path.exists(FILE_NAME):
        print("No expenses found.\n")
        return

    print("\n--- All Expenses ---")
    with open(FILE_NAME, "r") as file:
        for line in file:
            date, category, amount = line.strip().split(",")
            print(f"Date: {date} | Category: {category} | Amount: ₹{amount}")
    print()


def total_expense():
    if not os.path.exists(FILE_NAME):
        print("No expenses found.\n")
        return

    total = 0
    with open(FILE_NAME, "r") as file:
        for line in file:
            _, _, amount = line.strip().split(",")
            total += float(amount)

    print(f"\nTotal Expense: ₹{total}\n")


def menu():
    while True:
        print("===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expense")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expense()
        elif choice == "3":
            total_expense()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice!\n")


menu()
