
import csv
import uuid
from datetime import datetime

def parse_datetime(date_string):
    if date_string:
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

def calculate_pnl(order_type, open_price, close_price, volume):
    if order_type == 'Buy':
        return round((close_price - open_price) * volume * 10000, 2)
    return round((open_price - close_price) * volume * 10000, 2)

def generate_positions_csv(order_filename, position_filename):
    positions = {}
    all_positions = []
    with open(order_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            order_id = row['OrderID']
            account_id = row['AccountID']
            instrument = row['Instrument']
            order_type = row['OrderType']
            volume = float(row['Volume'])
            price = float(row['Price'])
            order_date = parse_datetime(row['OrderDate'])
            execution_date = parse_datetime(row['ExecutionDate'])
            status = row['Status']
            position_id = row['PositionID']
            if order_type == 'Buy':
                positions[position_id] = {'PositionID': position_id, 'AccountID': account_id, 'Instrument': instrument, 'Volume': volume, 'OpenPrice': price, 'OpenDate': order_date, 'Status': 'pending' if status != 'Executed' else 'open', 'OpenOrderID': order_id, 'ClosePrice': None, 'CloseDate': None, 'PnL': None, 'CloseOrderID': None}
            elif order_type == 'Sell' and position_id in positions and (positions[position_id]['Instrument'] == instrument):
                position = positions[position_id]
                position['ClosePrice'] = price
                position['CloseDate'] = execution_date
                position['Status'] = 'closed'
                position['PnL'] = calculate_pnl('Buy', position['OpenPrice'], price, volume)
                position['CloseOrderID'] = order_id
                all_positions.append(position)
                del positions[position_id]
        for position in positions.values():
            if position['Status'] == 'pending':
                position['Status'] = 'open'
            all_positions.append(position)
    with open(position_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['PositionID', 'AccountID', 'Instrument', 'Volume', 'OpenPrice', 'ClosePrice', 'OpenDate', 'CloseDate', 'PnL', 'Status', 'OpenOrderID', 'CloseOrderID'])
        for position in all_positions:
            writer.writerow([position['PositionID'], position['AccountID'], position['Instrument'], position['Volume'], position['OpenPrice'], position['ClosePrice'] if position['ClosePrice'] else '', position['OpenDate'].strftime('%Y-%m-%d %H:%M:%S'), position['CloseDate'].strftime('%Y-%m-%d %H:%M:%S') if position['CloseDate'] else '', position['Status'], position['OpenOrderID'], position['CloseOrderID'] if position['CloseOrderID'] else ''])

def generate_positions(filename, orders_filename):
    generate_positions_csv(orders_filename, filename)