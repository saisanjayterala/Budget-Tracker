import os
import csv
from datetime import datetime

class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.next_id = 1

    def add_income(self, description, amount):
        self.transactions.append({
            'id': self.next_id,
            'type': 'Income',
            'description': description,
            'amount': amount,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.next_id += 1

    def add_expense(self, description, amount):
        self.transactions.append({
            'id': self.next_id,
            'type': 'Expense',
            'description': description,
            'amount': amount,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.next_id += 1

    def calculate_balance(self):
        income = sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'Income')
        expenses = sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'Expense')
        return income, expenses, income - expenses

    def display_transactions(self):
        self.clear_screen()
        print(f"{'ID':<5} {'Type':<10} {'Description':<20} {'Amount':<10} {'Timestamp':<20}")
        print("="*70)
        for transaction in self.transactions:
            color = '\033[92m' if transaction['type'] == 'Income' else '\033[91m'
            reset = '\033[0m'
            print(f"{transaction['id']:<5} {color}{transaction['type']:<10}{reset} {transaction['description']:<20} {transaction['amount']:<10} {transaction['timestamp']:<20}")
        self.display_summary()

    def display_summary(self):
        income, expenses, balance = self.calculate_balance()
        print("="*70)
        print(f"\033[92mTotal Income:\033[0m ${income:.2f}")
        print(f"\033[91mTotal Expenses:\033[0m ${expenses:.2f}")
        print(f"\033[94mNet Balance:\033[0m ${balance:.2f}")
        print("="*70)

    def filter_transactions(self, transaction_type):
        return [t for t in self.transactions if t['type'] == transaction_type]

    def display_filtered_transactions(self, transaction_type):
        transactions = self.filter_transactions(transaction_type)
        if transactions:
            print(f"\n{transaction_type} Transactions:")
            print(f"{'ID':<5} {'Description':<20} {'Amount':<10} {'Timestamp':<20}")
            print("="*55)
            for transaction in transactions:
                print(f"{transaction['id']:<5} {transaction['description']:<20} {transaction['amount']:<10} {transaction['timestamp']:<20}")
        else:
            print(f"No {transaction_type.lower()} transactions found.")

    def input_amount(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    def confirm_action(self, action):
        confirmation = input(f"Are you sure you want to {action}? (yes/no): ").lower()
        return confirmation == 'yes'

    def edit_transaction(self, transaction_id):
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                if not self.confirm_action('edit this transaction'):
                    print("Edit cancelled.")
                    return
                print("Editing Transaction:")
                transaction['description'] = input("Enter new description: ")
                transaction['amount'] = self.input_amount("Enter new amount: ")
                transaction['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("Transaction updated.")
                return
        print("Transaction ID not found.")

    def delete_transaction(self, transaction_id):
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                if not self.confirm_action('delete this transaction'):
                    print("Delete cancelled.")
                    return
                self.transactions.remove(transaction)
                print("Transaction deleted.")
                return
        print("Transaction ID not found.")

    def search_transactions(self, search_term):
        results = [t for t in self.transactions if search_term.lower() in t['description'].lower() or search_term == str(t['amount'])]
        if results:
            print(f"\nSearch Results for '{search_term}':")
            print(f"{'ID':<5} {'Type':<10} {'Description':<20} {'Amount':<10} {'Timestamp':<20}")
            print("="*70)
            for transaction in results:
                color = '\033[92m' if transaction['type'] == 'Income' else '\033[91m'
                reset = '\033[0m'
                print(f"{transaction['id']:<5} {color}{transaction['type']:<10}{reset} {transaction['description']:<20} {transaction['amount']:<10} {transaction['timestamp']:<20}")
        else:
            print(f"No transactions found containing '{search_term}'.")

    def export_transactions(self, filename='transactions.csv'):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Type', 'Description', 'Amount', 'Timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for transaction in self.transactions:
                writer.writerow(transaction)
        print(f"Transactions exported to {filename}")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    tracker = BudgetTracker()
    
    while True:
        print("\n\033[95mBudget Tracker\033[0m")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. View All Transactions")
        print("5. View Income Transactions")
        print("6. View Expense Transactions")
        print("7. Edit a Transaction")
        print("8. Delete a Transaction")
        print("9. Search Transactions")
        print("10. Export Transactions to CSV")
        print("11. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            description = input("Enter income description: ")
            amount = tracker.input_amount("Enter income amount: ")
            tracker.add_income(description, amount)
        
        elif choice == '2':
            description = input("Enter expense description: ")
            amount = tracker.input_amount("Enter expense amount: ")
            tracker.add_expense(description, amount)
        
        elif choice == '3':
            income, expenses, balance = tracker.calculate_balance()
            print(f"\033[92mTotal Income:\033[0m ${income:.2f}")
            print(f"\033[91mTotal Expenses:\033[0m ${expenses:.2f}")
            print(f"\033[94mNet Balance:\033[0m ${balance:.2f}")
        
        elif choice == '4':
            tracker.display_transactions()
        
        elif choice == '5':
            tracker.display_filtered_transactions('Income')
        
        elif choice == '6':
            tracker.display_filtered_transactions('Expense')
        
        elif choice == '7':
            transaction_id = int(input("Enter the Transaction ID to edit: "))
            tracker.edit_transaction(transaction_id)
        
        elif choice == '8':
            transaction_id = int(input("Enter the Transaction ID to delete: "))
            tracker.delete_transaction(transaction_id)
        
        elif choice == '9':
            search_term = input("Enter a description or amount to search: ")
            tracker.search_transactions(search_term)
        
        elif choice == '10':
            tracker.export_transactions()
        
        elif choice == '11':
            print("Exiting the Budget Tracker.")
            break
        
        else:
            print("Invalid option. Please try again.")
