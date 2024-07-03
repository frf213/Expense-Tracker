import csv
import datetime
import sqlite3

def add_expense(expenses):
    while True:
        try:
            amount = float(input("Enter the amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    category = input("Enter the category: ")
    description = input("Enter the description (optional): ")
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    expenses.append({
        'Date': date_time,
        'Amount': amount,
        'Category': category,
        'Description': description
    })
    print("Expense added successfully!")

def display_expenses(expenses):
    if not expenses:
        print("No expenses to display.")
        return

    print("Expense List:")
    print("ID | Date                  | Amount | Category  | Description")
    print("-------------------------------------------------------------")
    for i, expense in enumerate(expenses, 1):
        print(f"{i}  | {expense['Date']} | {expense['Amount']}   | {expense['Category']} | {expense['Description']}")

def save_expenses_to_csv(expenses):
    if not expenses:
        print("No expenses to save.")
        return

    filename = input("Enter the filename to save: ")
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Amount', 'Category', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(expenses)

    print(f"Expenses saved successfully to '{filename}'!")

def create_connection():
    conn = sqlite3.connect('expenses.db')
    return conn

def create_table(conn):
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT
            );
        """)

def add_expense_db(conn):
    while True:
        try:
            amount = float(input("Enter the amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    category = input("Enter the category: ")
    description = input("Enter the description (optional): ")
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with conn:
        conn.execute("""
            INSERT INTO expenses (date, amount, category, description)
            VALUES (?, ?, ?, ?);
        """, (date_time, amount, category, description))
    print("Expense added successfully!")

def display_expenses_db(conn):
    cursor = conn.execute("SELECT id, date, amount, category, description FROM expenses;")
    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses to display.")
        return

    print("Expense List:")
    print("ID | Date                  | Amount | Category  | Description")
    print("-------------------------------------------------------------")
    for expense in expenses:
        print(f"{expense[0]}  | {expense[1]} | {expense[2]}   | {expense[3]} | {expense[4]}")

def save_expenses_to_csv_db(conn):
    cursor = conn.execute("SELECT date, amount, category, description FROM expenses;")
    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses to save.")
        return

    filename = input("Enter the filename to save: ")
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Amount', 'Category', 'Description']
        writer = csv.writer(csvfile)

        writer.writerow(fieldnames)
        writer.writerows(expenses)

    print(f"Expenses saved successfully to '{filename}'!")

def show_menu():
    print("\nExpense Tracker Menu:")
    print("1. Add Expense")
    print("2. Display Expenses")
    print("3. Save Expenses to CSV")
    print("4. Switch to SQLite" if mode == 'csv' else "4. Switch to CSV")
    print("5. Exit")
    print("Enter your choice (1/2/3/4/5): ")

def main_csv():
    expenses = []

    while True:
        show_menu()

        choice = input().strip()

        if choice == '1':
            add_expense(expenses)
        elif choice == '2':
            display_expenses(expenses)
        elif choice == '3':
            save_expenses_to_csv(expenses)
        elif choice == '4':
            return 'sqlite'
        elif choice == '5':
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    return 'exit'

def main_sqlite():
    conn = create_connection()
    create_table(conn)

    while True:
        show_menu()

        choice = input().strip()

        if choice == '1':
            add_expense_db(conn)
        elif choice == '2':
            display_expenses_db(conn)
        elif choice == '3':
            save_expenses_to_csv_db(conn)
        elif choice == '4':
            return 'csv'
        elif choice == '5':
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

    return 'exit'

if __name__ == "__main__":
    mode = 'csv'
    while True:
        if mode == 'csv':
            mode = main_csv()
        elif mode == 'sqlite':
            mode = main_sqlite()
        if mode == 'exit':
            break
