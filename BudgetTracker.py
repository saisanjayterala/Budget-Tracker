import os
import csv
from datetime import datetime

class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.next_id = 1
        self.categories = {}

    def add_income(self, description, amount, category='General'):
        self.transactions.append({
            'id': self.next_id,
            'type': 'Income',
            'description': description,
            'amount': amount,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'category': category
        })
        self.next_id += 1
        self.update_category(category, amount)

    def add_expense(self, description, amount, category='General'):
        self.transactions.append({
            'id': self.next_id,
            'type': 'Expense',
            'description': description,
            'amount': amount,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'category': category
        })
        self.next_id += 1
        self.update_category(category, -amount)
        self.check_budget(category)

    def calculate_balance(self):
        income = sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'Income')
        expenses = sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'Expense')
        return income, expenses, income - expenses

    def display_transactions(self):
        self.clear_screen()
        print(f"{'ID':<5} {'Type':<10} {'Description':<20} {'Amount':<10} {'Category':<15} {'Timestamp':<20}")
        print("="*85)
        for transaction in self.transactions:
            color = '\033[92m' if transaction['type'] == 'Income' else '\033[91m'
            reset = '\033[0m'
            print(f"{transaction['id']:<5} {color}{transaction['type']:<10}{reset} {transaction['description']:<20} {transaction['amount']:<10} {transaction['category']:<15} {transaction['timestamp']:<20}")
        self.display_summary()

    def display_summary(self):
        income, expenses, balance = self.calculate_balance()
        print("="*85)
        print(f"\033[92mTotal Income:\033[0m ${income:.2f}")
        print(f"\033[91mTotal Expenses:\033[0m ${expenses:.2f}")
        print(f"\033[94mNet Balance:\033[0m ${balance:.2f}")
        print("="*85)

    def update_category(self, category, amount):
        if category in self.categories:
            self.categories[category] += amount
        else:
            self.categories[category] = amount

    def display_category_summary(self):
        print("\nCategory Summary:")
        print(f"{'Category':<15} {'Balance':<10}")
        print("="*25)
        for category, balance in self.categories.items():
            color = '\033[92m' if balance >= 0 else '\033[91m'
            reset = '\033[0m'
            print(f"{color}{category:<15} ${balance:.2f}{reset}")
        print("="*25)

    def check_budget(self, category):
        if self.categories[category] < -500:
            print(f"\033[93mWarning:\033[0m You have exceeded the budget for {category}!")

    def filter_transactions(self, transaction_type):
        return [t for t in self.transactions if t['type'] == transaction_type]

    def display_filtered_transactions(self, transaction_type):
        transactions = self.filter_transactions(transaction_type)
        if transactions:
            print(f"\n{transaction_type} Transactions:")
            print(f"{'ID':<5} {'Description':<20} {'Amount':<10} {'Category':<15} {'Timestamp':<20}")
            print("="*70)
            for transaction in transactions:
                print(f"{transaction['id']:<5} {transaction['description']:<20} {transaction['amount']:<10} {transaction['category']:<15} {transaction['timestamp']:<20}")
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
                transaction['category'] = input("Enter new category: ")
                print("Transaction updated.")
                return
        print("Transaction ID not found.")

    def delete_transaction(self, transaction_id):
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                if not self.confirm_action('delete this transaction'):
                    print("Delete cancelled.")
                    return
                self.update_category(transaction['category'], -transaction['amount'])
                self.transactions.remove(transaction)
                print("Transaction deleted.")
                return
        print("Transaction ID not found.")

    def search_transactions(self, search_term):
        results = [t for t in self.transactions if search_term.lower() in t['description'].lower() or search_term == str(t['amount'])]
        if results:
            print(f"\nSearch Results for '{search_term}':")
            print(f"{'ID':<5} {'Type':<10} {'Description':<20} {'Amount':<10} {'Category':<15} {'Timestamp':<20}")
            print("="*85)
            for transaction in results:
                color = '\033[92m' if transaction['type'] == 'Income' else '\033[91m'
                reset = '\033[0m'
                print(f"{transaction['id']:<5} {color}{transaction['type']:<10}{reset} {transaction['description']:<20} {transaction['amount']:<10} {transaction['category']:<15} {transaction['timestamp']:<20}")
        else:
            print(f"No transactions found containing '{search_term}'.")

    def export_transactions(self, filename='transactions.csv'):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Type', 'Description', 'Amount', 'Category', 'Timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for transaction in self.transactions:
                writer.writerow(transaction)
        print(f"Transactions exported to {filename}")

    def save_data(self, filename='budget_data.csv'):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Type', 'Description', 'Amount', 'Category', 'Timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for transaction in self.transactions:
                writer.writerow(transaction)
        print(f"Data saved to {filename}")

    def load_data(self, filename='budget_data.csv'):
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                self.transactions = []
                self.categories = {}
                for row in reader:
                    row['amount'] = float(row['amount'])
                    self.transactions.append(row)
                    self.update_category(row['category'], row['amount'])
                    self.next_id = max(self.next_id, int(row['id']) + 1)
            print(f"Data loaded from {filename}")
        except FileNotFoundError:
            print(f"No data file found with the name {filename}")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    tracker = BudgetTracker()
    
    tracker.load_data()  # Load previous data if any

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
        print("11. View Category Summary")
        print("12. Save & Exit")
        print("0. Exit without Saving")

        choice = input("Select an option: ")

        if choice == '1':
            desc = input("Enter income description: ")
            amt = tracker.input_amount("Enter amount: ")
            category = input("Enter category: ")
            tracker.add_income(desc, amt, category)
        elif choice == '2':
            desc = input("Enter expense description: ")
            amt = tracker.input_amount("Enter amount: ")
            category = input("Enter category: ")
            tracker.add_expense(desc, amt, category)
        elif choice == '3':
            tracker.clear_screen()
            tracker.display_summary()
        elif choice == '4':
            tracker.display_transactions()
        elif choice == '5':
            tracker.display_filtered_transactions('Income')
        elif choice == '6':
            tracker.display_filtered_transactions('Expense')
        elif choice == '7':
            id_to_edit = int(input("Enter transaction ID to edit: "))
            tracker.edit_transaction(id_to_edit)
        elif choice == '8':
            id_to_delete = int(input("Enter transaction ID to delete: "))
            tracker.delete_transaction(id_to_delete)
        elif choice == '9':
            term = input("Enter search term: ")
            tracker.search_transactions(term)
        elif choice == '10':
            filename = input("Enter filename (default: transactions.csv): ")
            tracker.export_transactions(filename)
        elif choice == '11':
            tracker.display_category_summary()
        elif choice == '12':
            tracker.save_data()
            break
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")
