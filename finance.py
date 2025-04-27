import tkinter as tk
from tkinter import messagebox
import csv
import os

# File to store transactions
TRANSACTION_FILE = "finance_tracker.csv"

class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")

        # Labels and Entries for Income and Expenses
        self.amount_label = tk.Label(root, text="Amount ($):")
        self.amount_label.grid(row=0, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        self.category_label = tk.Label(root, text="Category:")
        self.category_label.grid(row=1, column=0)
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=1, column=1)

        self.type_label = tk.Label(root, text="Transaction Type:")
        self.type_label.grid(row=2, column=0)
        self.type_var = tk.StringVar()
        self.type_var.set("Income")
        self.income_radio = tk.Radiobutton(root, text="Income", variable=self.type_var, value="Income")
        self.income_radio.grid(row=2, column=1)
        self.expense_radio = tk.Radiobutton(root, text="Expense", variable=self.type_var, value="Expense")
        self.expense_radio.grid(row=2, column=2)

        self.add_button = tk.Button(root, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=3, column=0, columnspan=3)

        self.view_button = tk.Button(root, text="View Transactions", command=self.view_transactions)
        self.view_button.grid(row=4, column=0, columnspan=3)

        self.balance_label = tk.Label(root, text="Balance: $0.00")
        self.balance_label.grid(row=5, column=0, columnspan=3)

        # Load initial balance
        self.load_balance()

    def load_balance(self):
        """Load balance from the transactions in the CSV file"""
        if not os.path.exists(TRANSACTION_FILE):
            return 0.0
        balance = 0.0
        with open(TRANSACTION_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                amount = float(row[0])
                transaction_type = row[1]
                if transaction_type == "Income":
                    balance += amount
                elif transaction_type == "Expense":
                    balance -= amount
        self.update_balance(balance)

    def update_balance(self, balance):
        """Update the displayed balance"""
        self.balance_label.config(text=f"Balance: ${balance:.2f}")

    def add_transaction(self):
        """Add a new transaction to the tracker"""
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            transaction_type = self.type_var.get()

            if amount <= 0 or not category:
                messagebox.showerror("Invalid Input", "Please enter a valid amount and category.")
                return

            # Save transaction to CSV
            with open(TRANSACTION_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([amount, transaction_type, category])

            # Update balance
            self.load_balance()

            # Clear input fields
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)

            messagebox.showinfo("Success", f"{transaction_type} added successfully!")

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")

    def view_transactions(self):
        """View all transactions"""
        if not os.path.exists(TRANSACTION_FILE):
            messagebox.showinfo("No Transactions", "No transactions found.")
            return

        with open(TRANSACTION_FILE, "r") as file:
            reader = csv.reader(file)
            transactions = list(reader)

        if not transactions:
            messagebox.showinfo("No Transactions", "No transactions found.")
            return

        # Create a new window to display transactions
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("View Transactions")

        # Header row
        tk.Label(transaction_window, text="Amount ($)").grid(row=0, column=0)
        tk.Label(transaction_window, text="Type").grid(row=0, column=1)
        tk.Label(transaction_window, text="Category").grid(row=0, column=2)

        # Display each transaction
        for i, row in enumerate(transactions, 1):
            tk.Label(transaction_window, text=row[0]).grid(row=i, column=0)
            tk.Label(transaction_window, text=row[1]).grid(row=i, column=1)
            tk.Label(transaction_window, text=row[2]).grid(row=i, column=2)

# Create the main window
root = tk.Tk()

# Create the FinanceTracker object
finance_tracker = FinanceTracker(root)

# Run the app
root.mainloop()
