import os
import shutil
from clients import generate_clients
from accounts import generate_accounts
from orders import generate_orders
from trades import generate_trades
from transactions import generate_transactions
from commissions import generate_commissions
from reports import generate_reports
from positions import generate_positions
from risk_management import generate_risk_management
from currency import generate_currency_rates

# Define the target directory where CSV files are stored
TARGET_DIR = './out/'

# Function to clear the target directory
def clear_target_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)
    print(f"Cleared and recreated directory: {directory}")

# Function to run all generation functions with the specified number of records
def generate_all_data():
    print(f"Generating records for each dataset...")
    
    order_filename = f'{TARGET_DIR}/orders.csv'
    clients_filename = f'{TARGET_DIR}/clients.csv'
    accounts_filename = f'{TARGET_DIR}/accounts.csv'
    trades_filename = f'{TARGET_DIR}/trades.csv'
    transactions_filename = f'{TARGET_DIR}/transactions.csv'
    commissions_filename = f'{TARGET_DIR}/commissions.csv'
    reports_filename = f'{TARGET_DIR}/reports.csv'
    positions_filename = f'{TARGET_DIR}/positions.csv'
    risk_management_filename = f'{TARGET_DIR}/risk_management.csv'
    currency_filename = f'{TARGET_DIR}/currency.csv'

    # Call each generation function with size parameter
    generate_clients(clients_filename, 2000)
    generate_accounts(accounts_filename, clients_filename)
    generate_orders(order_filename, clients_filename, accounts_filename)
    generate_positions(positions_filename, order_filename)
    generate_trades(trades_filename, order_filename)
    generate_transactions(transactions_filename, order_filename, accounts_filename, clients_filename)
    generate_commissions(commissions_filename, transactions_filename)
    generate_reports(reports_filename, clients_filename, accounts_filename)
    generate_risk_management(risk_management_filename, accounts_filename, clients_filename, order_filename)
    generate_currency_rates(currency_filename, accounts_filename)
    print("Data generation completed.")

if __name__ == '__main__':
    clear_target_directory(TARGET_DIR)
    generate_all_data() 
