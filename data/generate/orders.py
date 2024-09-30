import csv
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta

# Инициализация Faker
fake = Faker()

# Возможные инструменты и их популярность
INSTRUMENTS = ['EUR/USD', 'GBP/USD', 'BTC/USD', 'AAPL', 'XAU/USD', 'TSLA', 'ETH/USD']
INSTRUMENT_WEIGHTS = [0.4, 0.2, 0.1, 0.1, 0.05, 0.1, 0.05]  # Вероятности для выбора инструмента

# Возможные статусы ордеров и их вероятность
ORDER_STATUSES = ['Executed', 'Cancelled', 'Partially Executed']
STATUS_WEIGHTS = [0.8, 0.1, 0.1]  # 80% - исполнены, 10% - отменены, 10% - частично исполнены

# Возможные стили трейдинга и их веса
TRADING_STYLES = ['Scalping', 'Day Trading', 'Swing Trading', 'Position Trading']
TRADING_STYLE_WEIGHTS = [0.3, 0.4, 0.2, 0.1]  # Вероятности для выбора стиля трейдинга

# Функция для генерации случайного объема ордера
def generate_order_volume():
    return round(random.uniform(0.01, 5), 2)  # Объем ордера (например, от 0.01 до 5 лотов)

# Функция для чтения данных из файла accounts.csv и клиентов (для даты регистрации)
def read_account_ids_and_clients(client_filename, account_filename):
    account_ids = []
    client_registration_dates = {}

    # Чтение данных клиентов
    with open(client_filename, mode='r', newline='', encoding='utf-8') as client_file:
        reader = csv.DictReader(client_file)
        for row in reader:
            # Преобразуем дату регистрации в объект datetime
            client_registration_dates[row['ClientID']] = datetime.strptime(row['RegistrationDate'], "%Y-%m-%d %H:%M:%S")

    # Чтение данных аккаунтов и добавление стиля трейдинга и даты регистрации клиента
    with open(account_filename, mode='r', newline='', encoding='utf-8') as account_file:
        reader = csv.DictReader(account_file)
        for row in reader:
            # Присваиваем стиль трейдинга на основе вероятностей
            trading_style = random.choices(TRADING_STYLES, weights=TRADING_STYLE_WEIGHTS, k=1)[0]
            account_ids.append({
                'AccountID': row['AccountID'],
                'ClientID': row['ClientID'],
                'RegistrationDate': client_registration_dates[row['ClientID']],  # Присваиваем дату регистрации как объект datetime
                'TradingStyle': trading_style  # Присваиваем стиль трейдинга
            })

    return account_ids

# Функция для генерации времени закрытия позиции в зависимости от стиля трейдинга
def generate_close_date(open_date, trading_style):
    if trading_style == 'Scalping':
        close_date = open_date + timedelta(minutes=random.randint(5, 60))  # Скальпинг: от 5 минут до 1 часа
    elif trading_style == 'Day Trading':
        close_date = open_date + timedelta(hours=random.randint(1, 8))  # Дейтрейдинг: от 1 до 8 часов
    elif trading_style == 'Swing Trading':
        close_date = open_date + timedelta(days=random.randint(2, 10))  # Свинг-трейдинг: от 2 до 10 дней
    else:  # Position Trading
        close_date = open_date + timedelta(weeks=random.randint(1, 12))  # Позиционный трейдинг: от 1 до 12 недель
    
    return close_date.strftime("%Y-%m-%d %H:%M:%S")

# Функция для генерации ордера
def generate_order(account, order_type, volume, instrument, position_id, open_date=None):
    order_id = str(uuid.uuid4())  # Уникальный идентификатор ордера
    
    price = round(random.uniform(1.0, 100.0), 5)  # Цена исполнения
    status = random.choices(ORDER_STATUSES, weights=STATUS_WEIGHTS, k=1)[0]  # Статус ордера на основе вероятностей
    commission = round(random.uniform(1, 50), 2)  # Комиссия за ордер
    order_date = open_date if open_date else fake.date_time_between(start_date=account['RegistrationDate'], end_date='now').strftime("%Y-%m-%d %H:%M:%S")  # Дата создания ордера
    execution_date = order_date if status == 'Executed' else ''  # Дата исполнения ордера (если исполнен)
    
    return [order_id, account['AccountID'], instrument, order_type, volume, price, status, order_date, execution_date, commission, position_id]

# Функция для генерации данных ордеров с учетом статусов и даты регистрации клиента
def generate_orders_and_positions_csv(filename, account_ids, num_positions):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Пишем заголовки
        writer.writerow(['OrderID', 'AccountID', 'Instrument', 'OrderType', 'Volume', 'Price', 'Status', 'OrderDate', 'ExecutionDate', 'Commission', 'PositionID'])

        for _ in range(num_positions):
            account = random.choice(account_ids)  # Случайный аккаунт из списка
            volume = generate_order_volume()  # Объем ордера
            position_id = str(uuid.uuid4())  # Идентификатор позиции
            instrument = random.choices(INSTRUMENTS, weights=INSTRUMENT_WEIGHTS, k=1)[0]  # Выбираем инструмент один раз для позиции

            # Распределяем тип позиции: 70-80% длинных и 20-30% коротких
            if random.random() < 0.75:  # 75% вероятности на длинную позицию
                # Длинная позиция: Buy -> Sell
                # Генерация ордера для открытия позиции (Buy)
                buy_order = generate_order(account, 'Buy', volume, instrument, position_id)
                writer.writerow(buy_order)

                # Генерация ордера для закрытия позиции (Sell) с учетом стиля трейдинга
                close_date = generate_close_date(datetime.strptime(buy_order[7], "%Y-%m-%d %H:%M:%S"), account['TradingStyle'])
                sell_order = generate_order(account, 'Sell', volume, instrument, position_id, open_date=close_date)
                writer.writerow(sell_order)

            else:
                # Короткая позиция: Sell -> Buy
                # Генерация ордера для открытия короткой позиции (Sell)
                sell_order = generate_order(account, 'Sell', volume, instrument, position_id)
                writer.writerow(sell_order)

                # Генерация ордера для закрытия короткой позиции (Buy) с учетом стиля трейдинга
                close_date = generate_close_date(datetime.strptime(sell_order[7], "%Y-%m-%d %H:%M:%S"), account['TradingStyle'])
                buy_order = generate_order(account, 'Buy', volume, instrument, position_id, open_date=close_date)
                writer.writerow(buy_order)

def generate_orders(filename, client_file_name, account_file_name, size):
    account_ids = read_account_ids_and_clients(client_file_name, account_file_name)
    generate_orders_and_positions_csv(filename, account_ids, size)