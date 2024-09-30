import csv
import uuid
import random
from faker import Faker
from datetime import datetime

# Инициализация Faker
fake = Faker()

# Функция для преобразования строки в объект datetime
def parse_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

# Функция для генерации объема сделки на основе ордера
def generate_trade_volume(order_volume, status):
    if status == 'Partially Executed':
        return round(random.uniform(0.01, order_volume), 2)  # Для частичного исполнения
    return order_volume  # Для полного исполнения

# Функция для генерации цены сделки на основе цены ордера
def generate_trade_price(order_price):
    price_variation = random.uniform(-0.01, 0.01)  # Допускаем небольшое отклонение
    return round(order_price + price_variation, 5)

# Функция для расчета прибыли/убытков на основе типа ордера и разницы в цене
def calculate_profit_loss(order_type, order_price, trade_price, volume):
    if order_type == 'Buy':
        return round((trade_price - order_price) * volume * 10000, 2)  # Пример расчета для валютных пар
    else:  # Для ордера Sell
        return round((order_price - trade_price) * volume * 10000, 2)

# Функция для расчета комиссии на основе объема сделки
def calculate_commission(volume):
    return round(volume * random.uniform(1, 5), 2)  # Комиссия за объем сделки

# Функция для чтения данных из файла orders.csv
def read_executed_orders_from_csv(filename):
    executed_orders = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Status'] in ['Executed', 'Partially Executed']:
                executed_orders.append({
                    'OrderID': row['OrderID'],
                    'Instrument': row['Instrument'],
                    'OrderType': row['OrderType'],
                    'OrderDate': parse_datetime(row['OrderDate']),
                    'Volume': float(row['Volume']),
                    'Price': float(row['Price']),
                    'Status': row['Status'],
                    'ExecutionDate': parse_datetime(row['ExecutionDate']) if row['ExecutionDate'] else None
                })
    return executed_orders

# Функция для генерации данных сделок
def generate_trades_csv(filename, executed_orders):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Пишем заголовки
        writer.writerow(['TradeID', 'OrderID', 'Instrument', 'TradeDate', 'Volume', 'Price', 'TradeType', 'ProfitLoss', 'Commission', 'Swap'])
        
        for order in executed_orders:
            # Если частично исполнен, создаем несколько сделок, иначе одну
            num_trades = random.randint(1, 3) if order['Status'] == 'Partially Executed' else 1
            
            for _ in range(num_trades):
                trade_id = str(uuid.uuid4())  # Уникальный идентификатор сделки
                trade_type = order['OrderType']  # Тип сделки соответствует типу ордера (Buy/Sell)
                volume = generate_trade_volume(order['Volume'], order['Status'])  # Объем сделки
                trade_price = generate_trade_price(order['Price'])  # Цена сделки на основе цены ордера
                profit_loss = calculate_profit_loss(order['OrderType'], order['Price'], trade_price, volume)  # Рассчитываем прибыль/убыток
                commission = calculate_commission(volume)  # Комиссия за сделку на основе объема
                swap = round(random.uniform(-10, 10), 2)  # Своп
                
                # Используем преобразованные даты
                trade_date = fake.date_time_between(
                    start_date=order['OrderDate'], 
                    end_date=order['ExecutionDate'] if order['ExecutionDate'] else 'now'
                ).strftime("%Y-%m-%d %H:%M:%S")  # Дата сделки, близкая к OrderDate и ExecutionDate
                
                # Записываем данные в CSV
                writer.writerow([trade_id, order['OrderID'], order['Instrument'], trade_date, volume, trade_price, trade_type, profit_loss, commission, swap])

# Генерация данных для сделок
def generate_trades(filename, order_filename):
    executed_orders = read_executed_orders_from_csv(order_filename)
    generate_trades_csv(filename, executed_orders)
