

import csv
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta
import pycountry
import numpy as np

fake = Faker()
FOREX_INSTRUMENTS = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'NZD/USD', 'USD/CHF']
CRYPTO_INSTRUMENTS = ['BTC/USD', 'ETH/USD', 'ADA/USD', 'SOL/USD', 'XRP/USD', 'DOGE/USD']
STOCKS_INSTRUMENTS = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'GOOGL', 'FB', 'NFLX']
COMMODITIES_INSTRUMENTS = ['XAU/USD', 'XAG/USD', 'WTI', 'BRENT']
CATEGORY_WEIGHTS = [0.4, 0.2, 0.3, 0.1]
ORDER_STATUSES = ['Executed', 'Cancelled', 'Partially Executed']
STATUS_WEIGHTS = [0.8, 0.1, 0.1]
TRADING_STYLES = ['Scalping', 'Day Trading', 'Swing Trading', 'Position Trading']
TRADING_STYLE_WEIGHTS = [0.3, 0.4, 0.2, 0.1]
LONG_POSITION_PROBABILITIES = {'Scalping': 0.6, 'Day Trading': 0.55, 'Swing Trading': 0.5, 'Position Trading': 0.65}
PRICE_PARAMETERS = {'Forex': {'mean': 1.2, 'stddev': 0.1}, 'Crypto': {'mean': 30000, 'stddev': 5000}, 'Stocks': {'mean': 200, 'stddev': 50}, 'Commodities': {'mean': 70, 'stddev': 20}}
COMMISSION_PARAMETERS = {'Forex': {'base': 1, 'rate': 0.0001}, 'Crypto': {'base': 5, 'rate': 0.0002}, 'Stocks': {'base': 2, 'rate': 0.0001}, 'Commodities': {'base': 3, 'rate': 0.00015}}

def generate_order_volume():
    return round(random.uniform(0.01, 5), 2)

def generate_instrument(trading_style):
    category = random.choices(['Forex', 'Crypto', 'Stocks', 'Commodities'], weights=CATEGORY_WEIGHTS, k=1)[0]
    if category == 'Forex':
        return (random.choice(FOREX_INSTRUMENTS), 'Forex')
    if category == 'Crypto':
        return (random.choice(CRYPTO_INSTRUMENTS), 'Crypto')
    if category == 'Stocks':
        return (random.choice(STOCKS_INSTRUMENTS), 'Stocks')
    return (random.choice(COMMODITIES_INSTRUMENTS), 'Commodities')

def read_account_ids_and_clients(client_filename, account_filename):
    account_ids = []
    client_registration_dates = {}
    with open(client_filename, mode='r', newline='', encoding='utf-8') as client_file:
        reader = csv.DictReader(client_file)
        for row in reader:
            client_registration_dates[row['ClientID']] = datetime.strptime(row['RegistrationDate'], '%Y-%m-%d %H:%M:%S')
    with open(account_filename, mode='r', newline='', encoding='utf-8') as account_file:
        reader = csv.DictReader(account_file)
        for row in reader:
            account_ids.append({'AccountID': row['AccountID'], 'ClientID': row['ClientID'], 'RegistrationDate': client_registration_dates[row['ClientID']], 'TradingStyle': row['TradingStyle']})
        return account_ids

def generate_close_date(open_date, trading_style):
    if trading_style == 'Scalping':
        close_date = open_date + timedelta(minutes=random.randint(5, 60))
    elif trading_style == 'Day Trading':
        close_date = open_date + timedelta(hours=random.randint(1, 8))
    elif trading_style == 'Swing Trading':
        close_date = open_date + timedelta(days=random.randint(2, 10))
    else:
        close_date = open_date + timedelta(weeks=random.randint(1, 12))
    return close_date.strftime('%Y-%m-%d %H:%M:%S')

def generate_order_price(category):
    mean = PRICE_PARAMETERS[category]['mean']
    stddev = PRICE_PARAMETERS[category]['stddev']
    price = max(0.01, round(np.random.normal(mean, stddev), 5))
    return price

def generate_order_commission(category, volume):
    base_commission = COMMISSION_PARAMETERS[category]['base']
    rate = COMMISSION_PARAMETERS[category]['rate']
    commission = round(base_commission + rate * volume, 2)
    return commission

def generate_order(account, order_type, volume, instrument, position_id, open_date=None):
    order_id = str(uuid.uuid4())
    instrument_name, category = instrument
    price = generate_order_price(category)
    status = random.choices(ORDER_STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
    commission = generate_order_commission(category, volume)
    order_date = open_date if open_date else fake.date_time_between(start_date=account['RegistrationDate'], end_date='now').strftime('%Y-%m-%d %H:%M:%S')
    execution_date = ''
    if status == 'Executed':
        execution_delay = timedelta(seconds=random.randint(1, 300))
        execution_date = (datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S') + execution_delay).strftime('%Y-%m-%d %H:%M:%S')
    return [order_id, account['AccountID'], instrument_name, order_type, volume, price, status, order_date, execution_date, commission, position_id]

def generate_orders_and_positions_csv(filename, account_ids):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['OrderID', 'AccountID', 'Instrument', 'OrderType', 'Volume', 'Price', 'Status', 'OrderDate', 'ExecutionDate', 'Commission', 'PositionID'])
        for account in account_ids:
            registration_duration = (datetime.now() - account['RegistrationDate']).days
            if account['TradingStyle'] == 'Scalping':
                num_orders = max(1, registration_duration // 5)
            elif account['TradingStyle'] == 'Day Trading':
                num_orders = max(1, registration_duration // 10)
            elif account['TradingStyle'] == 'Swing Trading':
                num_orders = max(1, registration_duration // 30)
            else:
                num_orders = max(1, registration_duration // 60)
            for _ in range(num_orders):
                volume = generate_order_volume()
                position_id = str(uuid.uuid4())
                instrument = generate_instrument(account['TradingStyle'])
                if random.random() < LONG_POSITION_PROBABILITIES[account['TradingStyle']]:
                    buy_order = generate_order(account, 'Buy', volume, instrument, position_id)
                    writer.writerow(buy_order)
                    close_date = generate_close_date(datetime.strptime(buy_order[7], '%Y-%m-%d %H:%M:%S'), account['TradingStyle'])
                    sell_order = generate_order(account, 'Sell', volume, instrument, position_id, open_date=close_date)
                    writer.writerow(sell_order)
                else:
                    sell_order = generate_order(account, 'Sell', volume, instrument, position_id)
                    writer.writerow(sell_order)
                    close_date = generate_close_date(datetime.strptime(sell_order[7], '%Y-%m-%d %H:%M:%S'), account['TradingStyle'])
                    buy_order = generate_order(account, 'Buy', volume, instrument, position_id, open_date=close_date)
                    writer.writerow(buy_order)

def generate_orders(filename, client_file_name, account_file_name):
    account_ids = read_account_ids_and_clients(client_file_name, account_file_name)
    generate_orders_and_positions_csv(filename, account_ids)