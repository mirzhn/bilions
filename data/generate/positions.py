import csv
import uuid
from datetime import datetime

# Функция для преобразования строки в объект datetime
def parse_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S") if date_string else None

# Функция для расчета прибыли/убытка по позиции
def calculate_pnl(order_type, open_price, close_price, volume):
    if order_type == 'Buy':  # Long position
        return round((close_price - open_price) * volume * 10000, 2)
    else:  # Short position (Sell)
        return round((open_price - close_price) * volume * 10000, 2)

# Функция для чтения ордеров и генерации позиций
def generate_positions_csv(order_filename, position_filename):
    positions = {}  # Хранение открытых позиций
    all_positions = []  # Список всех позиций для записи в CSV
    
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
            
            # Если это Buy, открываем позицию
            if order_type == 'Buy':
                positions[position_id] = {
                    'PositionID': position_id,
                    'AccountID': account_id,
                    'Instrument': instrument,
                    'Volume': volume,
                    'OpenPrice': price,
                    'OpenDate': order_date,
                    'Status': 'open',
                    'OpenOrderID': order_id,
                    'ClosePrice': None,
                    'CloseDate': None,
                    'PnL': None,
                    'CloseOrderID': None
                }
            
            # Если это Sell, закрываем позицию (проверяем наличие открытой позиции с тем же инструментом)
            elif order_type == 'Sell' and position_id in positions and positions[position_id]['Instrument'] == instrument:
                position = positions[position_id]
                
                # Закрываем позицию
                position['ClosePrice'] = price
                position['CloseDate'] = execution_date
                position['Status'] = 'closed'
                # Расчет PnL для long и short позиций
                position['PnL'] = calculate_pnl('Buy', position['OpenPrice'], price, volume)
                position['CloseOrderID'] = order_id
                
                # Добавляем закрытую позицию в список для записи
                all_positions.append(position)
                del positions[position_id]
        
        # Все незакрытые позиции сохраняем как открытые
        for position in positions.values():
            all_positions.append(position)
    
    # Записываем данные в positions.csv
    with open(position_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Пишем заголовки
        writer.writerow(['PositionID', 'AccountID', 'Instrument', 'Volume', 'OpenPrice', 'ClosePrice', 'OpenDate', 'CloseDate', 'PnL', 'Status', 'OpenOrderID', 'CloseOrderID'])
        
        for position in all_positions:
            writer.writerow([
                position['PositionID'],
                position['AccountID'],
                position['Instrument'],
                position['Volume'],
                position['OpenPrice'],
                position['ClosePrice'] if position['ClosePrice'] else '',
                position['OpenDate'].strftime("%Y-%m-%d %H:%M:%S"),
                position['CloseDate'].strftime("%Y-%m-%d %H:%M:%S") if position['CloseDate'] else '',
                position['PnL'] if position['PnL'] is not None else '',
                position['Status'],
                position['OpenOrderID'],
                position['CloseOrderID'] if position['CloseOrderID'] else ''
            ])

# Чтение данных ордеров и генерация позиций


def generate_positions(filename, orders_filename):
    generate_positions_csv(orders_filename, filename)