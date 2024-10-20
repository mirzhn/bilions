import csv
import uuid
import random
from faker import Faker
import pycountry
import numpy as np

fake = Faker()
ACCOUNT_TYPES = ['Real', 'Demo']
ACCOUNT_TYPE_WEIGHTS = [0.8, 0.2]
CURRENCIES = [currency.alpha_3 for currency in pycountry.currencies]
POPULAR_CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']
CURRENCY_WEIGHTS = []
for currency in CURRENCIES:
    if currency in POPULAR_CURRENCIES:
        CURRENCY_WEIGHTS.append(0.01)
    else:
        CURRENCY_WEIGHTS.append(0.001)
total_weight = sum(CURRENCY_WEIGHTS)
CURRENCY_WEIGHTS = [weight / total_weight for weight in CURRENCY_WEIGHTS]
TRADING_STYLES = ['Scalping', 'Day Trading', 'Swing Trading', 'Position Trading']
TRADING_STYLE_WEIGHTS = [0.1, 0.2, 0.4, 0.3]

def generate_balance(client_country):
    if client_country in ['United States', 'Germany', 'United Kingdom', 'France', 'Canada', 'Australia']:
        mean, sigma = (9, 1)
    else:
        mean, sigma = (8, 1.5)
    balance = round(np.random.lognormal(mean, sigma), 2)
    return min(balance, 1000000)

def generate_equity(balance, leverage):
    if leverage <= 50:
        equity = round(balance * random.uniform(0.9, 1.1), 2)
        return equity
    equity = round(balance * random.uniform(0.8, 1.2), 2)
    return equity

def generate_leverage(account_type):
    if account_type == 'Demo':
        mean, sigma = (100, 50)
    else:
        mean, sigma = (50, 20)
    leverage = max(1, min(int(np.random.normal(mean, sigma)), 200))
    return leverage

def generate_account_type():
    return random.choices(ACCOUNT_TYPES, weights=ACCOUNT_TYPE_WEIGHTS, k=1)[0]

def generate_currency(client_country):
    if client_country in ['United States']:
        return 'USD'
    if client_country in ['Eurozone', 'Germany', 'France']:
        return 'EUR'
    if client_country in ['United Kingdom']:
        return 'GBP'
    if client_country in ['Japan']:
        return 'JPY'
    if client_country in ['Australia']:
        return 'AUD'
    return random.choices(CURRENCIES, weights=CURRENCY_WEIGHTS, k=1)[0]

def generate_trading_style():
    return random.choices(TRADING_STYLES, weights=TRADING_STYLE_WEIGHTS, k=1)[0]

def read_client_ids_and_countries_from_csv(filename):
    client_data = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            client_data.append({'ClientID': row['ClientID'], 'Country': row['Country']})
        return client_data

def generate_accounts_csv(filename, client_data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['AccountID', 'ClientID', 'AccountType', 'Currency', 'Balance', 'Equity', 'Leverage', 'TradingStyle'])
        for client in client_data:
            client_id = client['ClientID']
            client_country = client['Country']
            num_accounts = random.randint(1, 3)
            for _ in range(num_accounts):
                account_id = str(uuid.uuid4())
                account_type = generate_account_type()
                currency = generate_currency(client_country)
                balance = generate_balance(client_country)
                leverage = generate_leverage(account_type)
                equity = generate_equity(balance, leverage)
                trading_style = generate_trading_style()
                writer.writerow([account_id, client_id, account_type, currency, balance, equity, leverage, trading_style])

def generate_accounts(filename, client_file_name):
    client_data = read_client_ids_and_countries_from_csv(client_file_name)
    generate_accounts_csv(filename, client_data)