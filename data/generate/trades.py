import csv
import uuid
import random
from faker import Faker
from datetime import datetime

fake = Faker()

def parse_datetime(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

def generate_trade_volume(order_volume, status):
    if status == 'Partially Executed':
        return round(order_volume * random.uniform(0.3, 0.7), 2)
    return order_volume

def generate_trade_price(order_price):
    price_variation = random.uniform(-0.05, 0.05)
    return round(order_price * (1 + price_variation), 5)

def calculate_profit_loss(order_type, order_price, trade_price, volume):
    if order_type == 'Buy':
        return round((trade_price - order_price) * volume * 10000, 2)
    return round((order_price - trade_price) * volume * 10000, 2)

def read_executed_orders_from_csv(filename):
    executed_orders = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Status'] in ['Executed', 'Partially Executed']:
                executed_orders.append({'OrderID': row['OrderID'], 'Instrument': row['Instrument'], 'OrderType': row['OrderType'], 'OrderDate': parse_datetime(row['OrderDate']), 'Volume': float(row['Volume']), 'Price': float(row['Price']), 'Status': row['Status'], 'ExecutionDate': parse_datetime(row['ExecutionDate']) if row['ExecutionDate'] else None, 'Commission': float(row['Commission'])})
        return executed_orders
        return executed_orders

def generate_swap(order_type, instrument, open_date, close_date):
    holding_period = (close_date - open_date).days + 1
    base_swap = {'Forex': {'Buy': -0.5, 'Sell': 0.5}, 'Crypto': {'Buy': -1.0, 'Sell': 1.0}, 'Stocks': {'Buy': -0.1, 'Sell': 0.1}, 'Commodities': {'Buy': -0.2, 'Sell': 0.2}}
    if instrument in ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'NZD/USD', 'USD/CHF']:
        category = 'Forex'
    elif instrument in ['BTC/USD', 'ETH/USD', 'ADA/USD', 'SOL/USD', 'XRP/USD', 'DOGE/USD']:
        category = 'Crypto'
    elif instrument in ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'GOOGL', 'FB', 'NFLX']:
        category = 'Stocks'
    else:
        category = 'Commodities'
    swap_rate = base_swap[category][order_type]
    swap = round(swap_rate * holding_period, 2)
    return swap

def generate_trades_csv(filename, executed_orders):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['TradeID', 'OrderID', 'Instrument', 'TradeDate', 'Volume', 'Price', 'TradeType', 'ProfitLoss', 'Commission', 'Swap'])
        for order in executed_orders:
            num_trades = random.randint(1, 3) if order['Status'] == 'Partially Executed' else 1
            for _ in range(num_trades):
                trade_id = str(uuid.uuid4())
                trade_type = order['OrderType']
                volume = generate_trade_volume(order['Volume'], order['Status'])
                trade_price = generate_trade_price(order['Price'])
                profit_loss = calculate_profit_loss(order['OrderType'], order['Price'], trade_price, volume)
                commission = order['Commission']
                trade_date = fake.date_time_between(start_date=order['OrderDate'], end_date=order['ExecutionDate'] if order['ExecutionDate'] else 'now')
                swap = generate_swap(order['OrderType'], order['Instrument'], order['OrderDate'], trade_date)
                trade_date_str = trade_date.strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([trade_id, order['OrderID'], order['Instrument'], trade_date_str, volume, trade_price, trade_type, profit_loss, commission, swap])

def generate_trades(filename, order_filename):
    executed_orders = read_executed_orders_from_csv(order_filename)
    generate_trades_csv(filename, executed_orders)