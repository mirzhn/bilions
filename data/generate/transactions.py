import csv
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta
fake = Faker()

TRANSACTION_TYPES = ['Deposit', 'Withdrawal', 'Bonus', 'Commission']
TRANSACTION_STATUSES = ['Completed', 'Pending', 'Failed']

def read_orders_by_account(filename):
    orders_by_account = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            account_id = row['AccountID']
            if account_id not in orders_by_account:
                orders_by_account[account_id] = []
            orders_by_account[account_id].append({'OrderID': row['OrderID'], 'Instrument': row['Instrument'], 'OrderType': row['OrderType'], 'Volume': float(row['Volume']), 'Price': float(row['Price']), 'Status': row['Status'], 'OrderDate': row['OrderDate'], 'ExecutionDate': row['ExecutionDate'], 'Commission': float(row['Commission']), 'PositionID': row['PositionID']})
        return orders_by_account
        return orders_by_account

def read_accounts_and_balances_from_csv(account_filename, client_filename):
    accounts = []
    client_registration_dates = {}
    with open(client_filename, mode='r', newline='', encoding='utf-8') as client_file:
        reader = csv.DictReader(client_file)
        for row in reader:
            client_registration_dates[row['ClientID']] = datetime.strptime(row['RegistrationDate'], '%Y-%m-%d %H:%M:%S')
    with open(account_filename, mode='r', newline='', encoding='utf-8') as account_file:
        reader = csv.DictReader(account_file)
        for row in reader:
            accounts.append({'AccountID': row['AccountID'], 'ClientID': row['ClientID'], 'Balance': float(row['Balance']), 'Currency': row['Currency'], 'RegistrationDate': client_registration_dates.get(row['ClientID'], None), 'ClientType': row.get('ClientType', 'New')})
        return accounts
        return accounts

def parse_datetime(date_string):
    if date_string:
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

def generate_initial_deposit(client_type):
    if client_type == 'VIP':
        return round(random.uniform(50000, 200000), 2)
    if client_type == 'Standard':
        return round(random.uniform(5000, 50000), 2)
    return round(random.uniform(1000, 5000), 2)

def generate_trade_pnl(order_volume, order_price, trade_price, order_type):
    if order_type == 'Buy':
        return round((trade_price - order_price) * order_volume * 10000, 2)
    return round((order_price - trade_price) * order_volume * 10000, 2)

def generate_bonus():
    return round(random.uniform(100, 1000), 2)

def generate_transactions_csv(filename, accounts, orders_by_account):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['TransactionID', 'AccountID', 'TransactionType', 'Amount', 'Currency', 'TransactionDate', 'Status', 'NewBalance'])
        for account in accounts:
            registration_date = account['RegistrationDate']
            currency = account['Currency']
            client_type = account['ClientType']
            initial_deposit = generate_initial_deposit(client_type)
            deposit_date = fake.date_time_between(start_date=registration_date, end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            account['Balance'] += initial_deposit
            writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Deposit', initial_deposit, currency, deposit_date, 'Completed', round(account['Balance'], 2)])
            account_orders = orders_by_account.get(account['AccountID'], [])
            for order in account_orders:
                execution_date = parse_datetime(order['ExecutionDate'])
                if execution_date is None or execution_date < registration_date:
                    continue
                commission = order['Commission']
                account['Balance'] -= commission
                writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Commission', commission, currency, order['OrderDate'], 'Completed', round(account['Balance'], 2)])
                trade_price = order['Price'] * random.uniform(0.95, 1.05)
                pnl = generate_trade_pnl(order['Volume'], order['Price'], trade_price, order['OrderType'])
                account['Balance'] += pnl
                writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Profit/Loss', pnl, currency, order['ExecutionDate'], 'Completed', round(account['Balance'], 2)])
                if random.random() < 0.1:
                    if account['Balance'] < 10000 or pnl < 0:
                        deposit_amount = generate_initial_deposit(client_type) / 10
                        account['Balance'] += deposit_amount
                        deposit_date = (execution_date + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Deposit', deposit_amount, currency, deposit_date, 'Completed', round(account['Balance'], 2)])
                    elif account['Balance'] > 50000 or pnl > 0:
                        withdrawal_amount = min(generate_initial_deposit(client_type) / 10, account['Balance'])
                        account['Balance'] -= withdrawal_amount
                        withdrawal_date = (execution_date + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Withdrawal', withdrawal_amount, currency, withdrawal_date, 'Completed', round(account['Balance'], 2)])
                if random.random() < 0.005:
                    bonus_amount = generate_bonus()
                    account['Balance'] += bonus_amount
                    bonus_date = (execution_date + timedelta(days=random.randint(1, 5))).strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Bonus', bonus_amount, currency, bonus_date, 'Completed', round(account['Balance'], 2)])

def generate_transactions(filename, order_filename, account_filename, client_filename):
    accounts = read_accounts_and_balances_from_csv(account_filename, client_filename)
    orders_by_account = read_orders_by_account(order_filename)
    generate_transactions_csv(filename, accounts, orders_by_account)