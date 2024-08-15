class BudgetTracker:
    def __init__(self):
        self.transactions = []

    def add_income(self, description, amount):
        self.transactions.append({'type': 'Income', 'description': description, 'amount': amount})

    def add_expense(self, description, amount):
        self.transactions.append({'type': 'Expense', 'description': description, 'amount': amount})

    def calculate_balance(self):
        income = sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'Income')
        expenses = sum(transaction['amount'] for transaction in self.transactions if transaction['type'] == 'Expense')
        return income - expenses

    def display_transactions(self):
        print(f"{'Type':<10} {'Description':<20} {'Amount':<10}")
        print("="*40)
        for transaction in self.transactions:
            print(f"{transaction['type']:<10} {transaction['description']:<20} {transaction['amount']:<10}")

if __name__ == "__main__":
    tracker = BudgetTracker()
    
    while True:
        print("\nBudget Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. View All Transactions")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            description = input("Enter income description: ")
            amount = float(input("Enter income amount: "))
            tracker.add_income(description, amount)
        
        elif choice == '2':
            description = input("Enter expense description: ")
            amount = float(input("Enter expense amount: "))
            tracker.add_expense(description, amount)
        
        elif choice == '3':
            balance = tracker.calculate_balance()
            print(f"Your current balance is: ${balance:.2f}")
        
        elif choice == '4':
            tracker.display_transactions()
        
        elif choice == '5':
            print("Exiting the Budget Tracker.")
            break
        
        else:
            print("Invalid option. Please try again.")
