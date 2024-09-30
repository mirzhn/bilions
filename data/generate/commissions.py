import csv
import uuid
import random
from faker import Faker
from datetime import datetime

# Инициализация Faker
fake = Faker()

# Возможные типы комиссий
COMMISSION_TYPES = ['Fixed', 'Dynamic']

# Функция для генерации типа комиссии на основе данных транзакции
def generate_commission_type():
    return random.choice(COMMISSION_TYPES)

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
            
            # Генерация данных для записи в файл commissions.csv
            writer.writerow([
                str(uuid.uuid4()),  # CommissionID
                transaction['TradeID'] if transaction['TradeID'] else str(uuid.uuid4()),  # Если нет TradeID, можно сгенерировать или найти
                transaction['AccountID'],  # AccountID
                'Instrument Placeholder',  # Инструмент, можно добавить связь с трейдом для получения инструмента
                commission_type,  # Тип комиссии (Fixed или Dynamic)
                transaction['Amount'],  # Сумма комиссии из транзакции
                transaction['TransactionDate']  # Дата комиссии из транзакции
            ])




def generate_commissions(filename, transactions_filename):
    # Чтение данных транзакций с типом "Commission" из файла transactions.csv
    transactions = read_commission_transactions_from_csv(transactions_filename)
    # Генерация данных для таблицы commissions на основе транзакций
    generate_commissions_csv(filename, transactions)