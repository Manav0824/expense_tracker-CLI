import argparse
import json
import os
from datetime import datetime
from tabulate import tabulate


DATA_FILE = "EXPENSES.json"

# Load data from file
def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save data to file
def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

# Add a new expense
def add_expense(description, amount):
    expenses = load_expenses()
    new_id = expenses[-1]['id'] + 1 if expenses else 1
    expense = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {new_id})")

# List all expenses
def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return

    table = [[e["id"], e["date"], e["description"], f"${e['amount']}"] for e in expenses]
    headers = ["ID", "Date", "Description", "Amount"]

    print(tabulate(table, headers, tablefmt="grid"))

    total = sum(e["amount"] for e in expenses)
    print(f"\n💰 Total Expenses: ${total}")



# Delete an expense
def delete_expense(expense_id):
    expenses = load_expenses()
    updated = [e for e in expenses if e["id"] != expense_id]
    if len(updated) == len(expenses):
        print("Error: Expense ID not found.")
    else:
        save_expenses(updated)
        print("Expense deleted successfully.")

# Show total summary
def show_summary(month=None):
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return

    now = datetime.now()
    current_month = now.month
    current_year = now.year

    # If no month is passed, show current month summary
    target_month = month if month else current_month

    total_expenses = sum(e["amount"] for e in expenses)
    monthly_expenses = [
        e for e in expenses
        if datetime.strptime(e["date"], "%Y-%m-%d").month == target_month
        and datetime.strptime(e["date"], "%Y-%m-%d").year == current_year
    ]
    monthly_total = sum(e["amount"] for e in monthly_expenses)

    if month:
        print(f"🗓 Total expenses for month {month}: ${monthly_total}")
    else:
        print(f"📅 Total expenses this month ({now.strftime('%B')}): ${monthly_total}")
        print(f"💸 Total expenses overall: ${total_expenses}")


# Argument parser
def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", type=float, required=True)

    # List
    subparsers.add_parser("list")

    # Delete
    del_parser = subparsers.add_parser("delete")
    del_parser.add_argument("--id", type=int, required=True)

    # Summary
    sum_parser = subparsers.add_parser("summary")
    sum_parser.add_argument("--month", type=int)

    args = parser.parse_args()

    if args.command == "add":
        if args.amount <= 0:
            print("Amount must be positive.")
        else:
            add_expense(args.description, args.amount)
    elif args.command == "list":
        list_expenses()
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "summary":
        show_summary(args.month)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
