import csv
import uuid
import random
from faker import Faker
from datetime import datetime

# Инициализация Faker
fake = Faker()

# Возможные типы комиссий и их веса
COMMISSION_TYPES = ['Fixed', 'Dynamic', 'Percentage', 'Tiered', 'Flat']
COMMISSION_WEIGHTS = [0.5, 0.2, 0.15, 0.1, 0.05]  # Вероятности для каждого типа комиссии

# Возможные инструменты и их веса
INSTRUMENTS = ['EUR/USD', 'GBP/USD', 'BTC/USD', 'AAPL', 'XAU/USD', 'TSLA', 'ETH/USD']
INSTRUMENT_WEIGHTS = [0.4, 0.2, 0.1, 0.1, 0.05, 0.1, 0.05]  # Вероятности для выбора инструмента

# Функция для генерации типа комиссии на основе данных транзакции с учетом вероятностей
def generate_commission_type():
    return random.choices(COMMISSION_TYPES, weights=COMMISSION_WEIGHTS, k=1)[0]

# Функция для генерации инструмента на основе вероятностей
def generate_instrument():
    return random.choices(INSTRUMENTS, weights=INSTRUMENT_WEIGHTS, k=1)[0]

# Функция для чтения данных транзакций с типом "Commission"
def read_commission_transactions_from_csv(filename):
    transactions = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['TransactionType'] == 'Commission':
                transactions.append({
                    'TransactionID': row['TransactionID'],
                    'AccountID': row['AccountID'],
                    'Amount': float(row['Amount']),
                    'Currency': row['Currency'],
                    'TransactionDate': row['TransactionDate'],
                    'TradeID': row['TradeID'] if 'TradeID' in row else None  # Можно добавить логику поиска TradeID, если нужно
                })
    return transactions

# Функция для генерации данных о комиссиях на основе транзакций
def generate_commissions_csv(filename, transactions):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Пишем заголовки
        writer.writerow(['CommissionID', 'TradeID', 'AccountID', 'Instrument', 'CommissionType', 'CommissionAmount', 'CommissionDate'])
        
        for transaction in transactions:
            # Генерация типа комиссии
            commission_type = generate_commission_type()

            # Генерация инструмента
            instrument = generate_instrument()
            
            # Генерация данных для записи в файл commissions.csv
            writer.writerow([
                str(uuid.uuid4()),  # CommissionID
                transaction['TradeID'] if transaction['TradeID'] else str(uuid.uuid4()),  # Если нет TradeID, можно сгенерировать или найти
                transaction['AccountID'],  # AccountID
                instrument,  # Сгенерированный инструмент
                commission_type,  # Тип комиссии (Fixed, Dynamic, Percentage, Tiered, Flat)
                transaction['Amount'],  # Сумма комиссии из транзакции
                transaction['TransactionDate']  # Дата комиссии из транзакции
            ])

def generate_commissions(filename, transactions_filename):
    # Чтение данных транзакций с типом "Commission" из файла transactions.csv
    transactions = read_commission_transactions_from_csv(transactions_filename)
    # Генерация данных для таблицы commissions на основе транзакций
    generate_commissions_csv(filename, transactions)


#generate_commissions('./out/commissions.csv', './out/transactions.csv')