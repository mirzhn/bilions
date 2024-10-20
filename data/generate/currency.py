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

# Функция для генерации типа комиссии на основе данных транзакции с учетом вероятностей
def generate_commission_type():
    return random.choices(COMMISSION_TYPES, weights=COMMISSION_WEIGHTS, k=1)[0]

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
        writer.writerow(['CommissionID', 'TransactionID', 'AccountID', 'CommissionType', 'CommissionAmount', 'CommissionDate'])
        
        for transaction in transactions:
            # Генерация типа комиссии
            commission_type = generate_commission_type()
            
            # Генерация данных для записи в файл commissions.csv
            writer.writerow([
                str(uuid.uuid4()),  # CommissionID
                transaction['TransactionID'],  # Используем TransactionID вместо TradeID
                transaction['AccountID'],  # AccountID
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
