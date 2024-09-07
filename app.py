import os
import csv
import numpy as np 
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# File names
USER_FILE = "users.csv"
BRANCHES_FILE = "branches.csv"
PRODUCTS_FILE = "products.csv"
SALES_FILE = "sales.csv"

# Factory Pattern

# Interface for data loaders
class DataLoader: 
    def load_data(self):
        raise NotImplementedError

# CSV loader implementation
class CSVLoader(DataLoader):
    def __init__(self, file_name):
        self.file_name = file_name
    
    def load_data(self):
        data = []
        if os.path.exists(self.file_name):
            with open(self.file_name, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    data.append(row)
        return data

# Factory to create loaders
class DataLoaderFactory:
    @staticmethod
    def create_loader(file_name):
        if file_name.endswith('users.csv'):
            return CSVLoader(file_name)
        elif file_name.endswith('branches.csv'):
            return CSVLoader(file_name)
        elif file_name.endswith('products.csv'):
            return CSVLoader(file_name)
        elif file_name.endswith('sales.csv'):
            return CSVLoader(file_name)
        else:
            raise ValueError("Unsupported file type")

# Command Pattern

# Base command interface
class Command:
    def execute(self):
        raise NotImplementedError

# Concrete command to add a new branch
class AddBranchCommand(Command):
    def execute(self):
        print("\n>>>>> Add New Branch <<<<<")
        branches = load_data(BRANCHES_FILE)
        
        branch_id = input("Enter Branch ID: ")
        branch_name = input("Enter Branch Name: ")
        location = input("Enter Location: ")

        new_branch = [branch_id, branch_name, location]
        branches.append(new_branch)

        os.remove(BRANCHES_FILE)

        headers = ['Branch ID', 'Branch Name', 'Location']
        save_data(BRANCHES_FILE, branches, headers=headers)
        print(f"Branch '{branch_name}' added successfully.")

# Concrete command to add a new sale
class AddSaleCommand(Command):
    def execute(self):
        print("\n>>>>> Add New Sale <<<<<")
        sales = load_data(SALES_FILE)
        
        branch_id = input("Enter Branch ID: ")
        product_id = input("Enter Product ID: ")
        amount_sold = input("Enter Amount Sold: ")

        new_sale = [branch_id, product_id, amount_sold, datetime.now().strftime('%Y-%m-%d')]
        sales.append(new_sale)

        os.remove(SALES_FILE)

        headers = ['Branch ID', 'Product ID', 'Amount Sold', 'Date']
        save_data(SALES_FILE, sales, headers=headers)
        print("Sale added successfully.")

# Concrete command for monthly sales analysis of a specific branch
class MonthlySalesAnalysisCommand(Command):
    def __init__(self, branch_id):
        self.branch_id = branch_id
    
    def execute(self):
        monthly_sales_analysis(self.branch_id)

# Concrete command for price analysis of a specific product
class PriceAnalysisCommand(Command):
    def __init__(self, product_id):
        self.product_id = product_id
    
    def execute(self):
        price_analysis(self.product_id)

# Concrete command for weekly sales analysis of the supermarket network
class WeeklySalesAnalysisCommand(Command):
    def execute(self):
        weekly_sales_analysis()

# Concrete command for total sales amount analysis
class TotalSalesAmountAnalysisCommand(Command):
    def execute(self):
        total_sales_amount_analysis()

# Concrete command for monthly sales analysis of all branches
class AllBranchesMonthlySalesAnalysisCommand(Command):
    def execute(self):
        all_branches_monthly_sales_analysis()

# Utility Functions

# Function to load data from CSV file
def load_data(file_name):
    loader = DataLoaderFactory.create_loader(file_name)
    return loader.load_data()

# Function to save data to CSV file
def save_data(file_name, data, headers=None):
    file_exists = os.path.exists(file_name)
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists and headers:
            writer.writerow(headers)
        writer.writerows(data)

# Function for user login
def login():
    print(">>>>> Login <<<<<")
    username = input("Enter username: ")
    password = input("Enter password: ")
    with open(USER_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True
    return False

# Function for monthly sales analysis of a specific branch
def monthly_sales_analysis(branch_id):
    print(f"\n>>>>> Monthly Sales Analysis - Branch {branch_id} <<<<<")
    sales_data = load_data(SALES_FILE)
    branch_sales = [int(sale[2]) for sale in sales_data if sale[0] == branch_id]

    if not branch_sales:
        print(f"No sales data found for Branch ID {branch_id}.")
        return

    # Generate a histogram for monthly sales
    plt.figure(figsize=(8, 5))
    plt.hist(branch_sales, bins=10, edgecolor='black')
    plt.title(f'Monthly Sales Analysis - Branch {branch_id}')
    plt.xlabel('Sales Amount (LKR)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# Function for price analysis of a specific product
def price_analysis(product_id):
    print(f"\n>>>>> Price Analysis - Product {product_id} <<<<<")
    sales_data = load_data(SALES_FILE)
    product_sales = [int(sale[2]) for sale in sales_data if sale[1] == product_id]

    if not product_sales:
        print(f"No sales data found for Product ID {product_id}.")
        return

    average_price = np.mean(product_sales)
    max_price = np.max(product_sales)
    min_price = np.min(product_sales)
    median_price = np.median(product_sales)

    print(f"Average Price: {average_price} LKR")
    print(f"Maximum Price: {max_price} LKR")
    print(f"Minimum Price: {min_price} LKR")
    print(f"Median Price: {median_price} LKR")

    # Plotting boxplot for price distribution
    plt.figure(figsize=(8, 5))
    plt.boxplot(product_sales, vert=False)
    plt.title(f'Price Distribution - Product {product_id}')
    plt.xlabel('Sales Amount (LKR)')
    plt.grid(True)
    plt.show()

# Function for weekly sales analysis of the supermarket network
def parse_date(date_str):
    for fmt in ('%Y-%m-%d', '%m/%d/%Y'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f"time data '{date_str}' does not match any known format")

def weekly_sales_analysis():
    print("\n>>>>> Weekly Sales Analysis - Supermarket Network <<<<<")
    sales_data = load_data(SALES_FILE)

    # Example: Analyze sales for the current week
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    weekly_sales = [int(sale[2]) for sale in sales_data
                    if start_of_week <= parse_date(sale[3]) <= end_of_week]

    total_sales = sum(weekly_sales)
    average_sales = np.mean(weekly_sales) if weekly_sales else 0

    print(f"Total Sales for the Week: {total_sales} LKR")
    print(f"Average Daily Sales: {average_sales} LKR")

# Function for total sales amount analysis
def total_sales_amount_analysis():
    print("\n>>>>> Total Sales Amount Analysis <<<<<")
    sales_data = load_data(SALES_FILE)
    total_sales = sum([int(sale[2]) for sale in sales_data])

    print(f"Total Sales Amount: {total_sales} LKR")

# Function for monthly sales analysis of all branches
def all_branches_monthly_sales_analysis():
    print("\n>>>>> Monthly Sales Analysis of All Branches <<<<<")
    sales_data = load_data(SALES_FILE)
    branches = load_data(BRANCHES_FILE)
    
    monthly_sales = {branch[0]: 0 for branch in branches}
    
    for sale in sales_data:
        branch_id = sale[0]
        monthly_sales[branch_id] += int(sale[2])
    
    branch_ids, sales_amounts = zip(*monthly_sales.items())
    
    plt.figure(figsize=(10, 6))
    plt.bar(branch_ids, sales_amounts)
    plt.title('Monthly Sales Analysis of All Branches')
    plt.xlabel('Branch ID')
    plt.ylabel('Total Sales (LKR)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Main Program 

# Main program loop with command execution
def main():
    # Ensure CSV files exist with headers
    headers_users = ['Username', 'Password']
    if not os.path.exists(USER_FILE):
        save_data(USER_FILE, [], headers=headers_users)

    headers_branches = ['Branch ID', 'Branch Name', 'Location']
    if not os.path.exists(BRANCHES_FILE):
        save_data(BRANCHES_FILE, [], headers=headers_branches)

    headers_products = ['Product ID', 'Product Name']
    if not os.path.exists(PRODUCTS_FILE):
        save_data(PRODUCTS_FILE, [], headers=headers_products)

    headers_sales = ['Branch ID', 'Product ID', 'Amount Sold', 'Date']
    if not os.path.exists(SALES_FILE):
        save_data(SALES_FILE, [], headers=headers_sales)

    # Login loop
    while True:
        if login():
            print("Login successful!")
            break
        else:
            print("Invalid credentials. Please try again.")

    # Command map
    commands = {
        '1': AddBranchCommand,
        '2': AddSaleCommand,
        '3': MonthlySalesAnalysisCommand,
        '4': PriceAnalysisCommand,
        '5': WeeklySalesAnalysisCommand,
        '6': TotalSalesAmountAnalysisCommand,
        '7': AllBranchesMonthlySalesAnalysisCommand,
        '8': lambda: print("Logged out.")
    }

    # Main menu
    while True:
        print("\n>>>>>> Main Menu <<<<<<")
        print("1. Add a New Branch")
        print("2. Add a New Sale")
        print("3. Monthly Sales Analysis of a Specific Branch")
        print("4. Price Analysis of a Specific Product")
        print("5. Weekly Sales Analysis of Supermarket Network")
        print("6. Analysis of Total Sales Amounts of Purchases")
        print("7. Monthly Sales Analysis of All Branches")
        print("8. Log out")

        choice = input("Enter your choice (1-8): ")

        if choice in commands:
            if choice == '8':
                commands[choice]()  # Log out directly
                break
            else:
                if choice in ['3', '4']:
                    param = input(f"Enter {'Branch ID' if choice == '3' else 'Product ID'}: ")
                    command = commands[choice](param)
                else:
                    command = commands[choice]()
                command.execute()
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

# Execute the main program
if __name__ == "__main__":
    main()
