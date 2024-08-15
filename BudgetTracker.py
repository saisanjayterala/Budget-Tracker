class BudgetTracker:
    def __init__(self):
        self.transactions = []
        self.next_id = 1  # Initialize transaction ID counter

    def add_income(self, description, amount):
        self.transactions.append({'id': self.next_id, 'type': 'Income', 'description': description, 'amount': amount})
        self.next_id += 1

    def add_expense(self, description, amount):
        self.transactions.append({'id': self.next_id, 'type': 'Expense', 'description': description, 'amount': amount})
        self.next_id += 1

    def calculate_balance(self):
        income = sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'Income')
        expenses = sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'Expense')
        return income - expenses

    def display_transactions(self):
        print(f"{'ID':<5} {'Type':<10} {'Description':<20} {'Amount':<10}")
        print("="*50)
        for transaction in self.transactions:
            print(f"{transaction['id']:<5} {transaction['type']:<10} {transaction['description']:<20} {transaction['amount']:<10}")

    def filter_transactions(self, transaction_type):
        return [t for t in self.transactions if t['type'] == transaction_type]

    def display_filtered_transactions(self, transaction_type):
        transactions = self.filter_transactions(transaction_type)
        if transactions:
            print(f"\n{transaction_type} Transactions:")
            print(f"{'ID':<5} {'Description':<20} {'Amount':<10}")
            print("="*35)
            for transaction in transactions:
                print(f"{transaction['id']:<5} {transaction['description']:<20} {transaction['amount']:<10}")
        else:
            print(f"No {transaction_type.lower()} transactions found.")

    def input_amount(self, prompt):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    def edit_transaction(self, transaction_id):
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                print("Editing Transaction:")
                transaction['description'] = input("Enter new description: ")
                transaction['amount'] = self.input_amount("Enter new amount: ")
                print("Transaction updated.")
                return
        print("Transaction ID not found.")

    def delete_transaction(self, transaction_id):
        for transaction in self.transactions:
            if transaction['id'] == transaction_id:
                self.transactions.remove(transaction)
                print("Transaction deleted.")
                return
        print("Transaction ID not found.")

if __name__ == "__main__":
    tracker = BudgetTracker()
    
    while True:
        print("\nBudget Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. View All Transactions")
        print("5. View Income Transactions")
        print("6. View Expense Transactions")
        print("7. Edit a Transaction")
        print("8. Delete a Transaction")
        print("9. Exit")
        
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
            balance = tracker.calculate_balance()
            print(f"Your current balance is: ${balance:.2f}")
        
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
            print("Exiting the Budget Tracker.")
            break
        
        else:
            print("Invalid option. Please try again.")
