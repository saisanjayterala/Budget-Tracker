# Budget-Tracker

A Python-based Budget Tracker application that helps users manage their income, expenses, and track their financial transactions. It supports multiple user profiles, data encryption for security, and provides graphical reports for a better understanding of your financial situation.
![image](https://github.com/user-attachments/assets/b5660be9-5deb-4880-a407-8671bc0bed47)

## Features

- **Income and Expense Management:** Add, view, and manage income and expenses across various categories.
- **User Profiles:** Create and switch between multiple user profiles.
- **Recurring Transactions:** Set up and manage recurring income or expense transactions.
- **Budget Categories:** Categorize transactions and track spending in different categories.
- **Data Encryption:** Secure sensitive data using encryption (Fernet encryption from the cryptography library).
- **Graphical Reports:** Generate monthly income and expense reports using matplotlib.
- **CSV Export/Import:** Save and load your transactions to/from a CSV file.
- **User Authentication:** Basic user authentication for profile access.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/saisanjayterala/Budget-Tracker_python.git
   cd Budget-Tracker_python

2 .Install the required packages:

Make sure you have Python 3 installed. Then, install the required packages using pip

3 .Run the application:
```
python budget_tracker.py
```


## Usage

Upon running the application, you will be presented with a menu of options. You can perform the following actions:

- **Add Income** - Record a new income transaction.
- **Add Expense** - Record a new expense transaction.
- **View Balance** - Display the current income, expenses, and net balance.
- **View All Transactions** - Display a list of all transactions.
- **View Income Transactions** - Filter and display only income transactions.
- **View Expense Transactions** - Filter and display only expense transactions.
- **Edit a Transaction** - Edit an existing transaction by ID.
- **Delete a Transaction** - Delete a transaction by ID.
- **Search Transactions** - Search for transactions by description.
- **Export Transactions** - Save all transactions to a CSV file.
- **View Category Summary** - View a summary of balances by category.
- **Add Profile** - Create a new user profile.
- **Switch Profile** - Switch to a different user profile.
- **Add Recurring Transaction** - Add a recurring income or expense.
- **Generate Graphical Report** - Generate a monthly income and expense report.
- **Save Data** - Save all data to a CSV file.
- **Authenticate User** - Authenticate and switch profiles.
- **Exit** - Exit the application.
