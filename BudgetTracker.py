import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.next_id = 1
        self.categories = defaultdict(float)
        self.profiles = {}
        self.current_profile = 'default'
        self.recurring_transactions = defaultdict(list)
        self.budgets = defaultdict(float)

    def add_income(self, description, amount, category='General'):
        transaction = {
            'id': self.next_id,
            'type': 'Income',
            'description': description,
            'amount': amount,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'category': category,
            'profile': self.current_profile
        }
        self.transactions.append(transaction)
        self.next_id += 1
        self.categories[category] += amount
        self.update_budget(category, amount)
        self.check_budget(category)

    def add_expense(self, description, amount, category='General'):
        transaction = {
            'id': self.next_id,
            'type': 'Expense',
            'description': description,
            'amount': amount,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'category': category,
            'profile': self.current_profile
        }
        self.transactions.append(transaction)
        self.next_id += 1
        self.categories[category] -= amount
        self.update_budget(category, -amount)
        self.check_budget(category)

    def update_budget(self, category, amount):
        if category in self.budgets:
            self.budgets[category] += amount
        else:
            self.budgets[category] = amount

    def check_budget(self, category):
        if category in self.budgets and self.budgets[category] < -500:
            print(f"\033[93mWarning:\033[0m You have exceeded the budget for {category}!")

    def calculate_balance(self):
        income = sum(t['amount'] for t in self.transactions if t['type'] == 'Income' and t['profile'] == self.current_profile)
        expenses = sum(t['amount'] for t in self.transactions if t['type'] == 'Expense' and t['profile'] == self.current_profile)
        return income, expenses, income - expenses

    def display_transactions(self):
        self.clear_screen()
        print(f"{'ID':<5} {'Type':<10} {'Description':<20} {'Amount':<10} {'Category':<15} {'Timestamp':<20}")
        print("="*85)
        for t in self.transactions:
            if t['profile'] == self.current_profile:
                color = '\033[92m' if t['type'] == 'Income' else '\033[91m'
                reset = '\033[0m'
                print(f"{t['id']:<5} {color}{t['type']:<10}{reset} {t['description']:<20} {t['amount']:<10} {t['category']:<15} {t['timestamp']:<20}")
        self.display_summary()

    def display_summary(self):
        income, expenses, balance = self.calculate_balance()
        print("="*85)
        print(f"\033[92mTotal Income:\033[0m ${income:.2f}")
        print(f"\033[91mTotal Expenses:\033[0m ${expenses:.2f}")
        print(f"\033[94mNet Balance:\033[0m ${balance:.2f}")
        print("="*85)

    def display_category_summary(self):
        print("\nCategory Summary:")
        print(f"{'Category':<15} {'Balance':<10}")
        print("="*25)
        for category, balance in self.categories.items():
            color = '\033[92m' if balance >= 0 else '\033[91m'
            reset = '\033[0m'
            print(f"{color}{category:<15} ${balance:.2f}{reset}")
        print("="*25)

    def display_profile_summary(self):
        print("\nUser Profiles Summary:")
        for profile, data in self.profiles.items():
            print(f"{profile}: Total Balance: ${data['balance']:.2f}")
        print("="*25)

    def add_profile(self, profile_name):
        if profile_name not in self.profiles:
            self.profiles[profile_name] = {'balance': 0}
            print(f"Profile '{profile_name}' added.")
        else:
            print(f"Profile '{profile_name}' already exists.")

    def switch_profile(self, profile_name):
        if profile_name in self.profiles:
            self.current_profile = profile_name
            print(f"Switched to profile '{profile_name}'.")
        else:
            print(f"Profile '{profile_name}' does not exist.")

    def add_recurring_transaction(self, transaction_type, description, amount, category='General', interval='monthly'):
        self.recurring_transactions[self.current_profile].append({
            'type': transaction_type,
            'description': description,
            'amount': amount,
            'category': category,
            'interval': interval
        })

    def process_recurring_transactions(self):
        for transaction in self.recurring_transactions[self.current_profile]:
            if transaction['interval'] == 'monthly':
                self.add_income(transaction['description'], transaction['amount'], transaction['category']) if transaction['type'] == 'Income' else self.add_expense(transaction['description'], transaction['amount'], transaction['category'])

    def generate_graphical_report(self):
        income = defaultdict(float)
        expenses = defaultdict(float)

        for t in self.transactions:
            if t['profile'] == self.current_profile:
                month = t['timestamp'][:7]
                if t['type'] == 'Income':
                    income[month] += t['amount']
                else:
                    expenses[month] += t['amount']

        months = sorted(set(income.keys()).union(expenses.keys()))
        income_values = [income.get(month, 0) for month in months]
        expense_values = [expenses.get(month, 0) for month in months]

        plt.figure(figsize=(10, 5))
        plt.plot(months, income_values, label='Income', color='green')
        plt.plot(months, expense_values, label='Expenses', color='red')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.title('Monthly Income and Expenses')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def save_data(self, filename='budget_data.csv'):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Type', 'Description', 'Amount', 'Category', 'Timestamp', 'Profile']
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
                self.categories = defaultdict(float)
                for row in reader:
                    row['amount'] = float(row['amount'])
                    self.transactions.append(row)
                    self.categories[row['category']] += row['amount']
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
        print("12. Add Profile")
        print("13. Switch Profile")
        print("14. Add Recurring Transaction")
        print("15. Generate Graphical Report")
        print("16. Save & Exit")
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
            profile_name = input("Enter new profile name: ")
            tracker.add_profile(profile_name)
        elif choice == '13':
            profile_name = input("Enter profile name to switch to: ")
            tracker.switch_profile(profile_name)
        elif choice == '14':
            transaction_type = input("Enter transaction type (Income/Expense): ")
            desc = input("Enter description: ")
            amt = tracker.input_amount("Enter amount: ")
            category = input("Enter category: ")
            interval = input("Enter interval (monthly/weekly): ")
            tracker.add_recurring_transaction(transaction_type, desc, amt, category, interval)
        elif choice == '15':
            tracker.generate_graphical_report()
        elif choice == '16':
            tracker.save_data()
            break
        elif choice == '0':
            break
        else:
            print("Invalid option. Please try again.")
