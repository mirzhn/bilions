import csv
import uuid
import random
from faker import Faker
from datetime import datetime

# Инициализация Faker
fake = Faker()

# Возможные типы транзакций
TRANSACTION_TYPES = ['Deposit', 'Withdrawal', 'Bonus', 'Commission']

# Возможные статусы транзакций
TRANSACTION_STATUSES = ['Completed', 'Pending', 'Failed']

# Функция для генерации начального депозита
def generate_initial_deposit():
    return round(random.uniform(1000, 50000), 2)  # Начальный депозит от 1000 до 50000

# Функция для генерации прибыли/убытков (PnL) для сделок
def generate_trade_pnl():
    return round(random.uniform(-1000, 5000), 2)  # Прибыль/убыток от -1000 до 5000

# Функция для генерации комиссии
def generate_commission():
    return round(random.uniform(5, 50), 2)  # Комиссия от 5 до 50

# Функция для чтения данных ордеров из orders.csv
def read_orders_from_csv(filename):
    orders = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            orders.append({
                'OrderID': row['OrderID'],
                'AccountID': row['AccountID'],
                'Instrument': row['Instrument'],
                'OrderType': row['OrderType'],
                'Volume': float(row['Volume']),
                'Price': float(row['Price']),
                'Status': row['Status'],
                'OrderDate': row['OrderDate'],
                'ExecutionDate': row['ExecutionDate'],
                'Commission': float(row['Commission']),
                'PositionID': row['PositionID']
            })
    return orders

# Функция для чтения данных из файла accounts.csv и возврата балансов
def read_accounts_and_balances_from_csv(account_filename, client_filename):
    accounts = []
    # Чтение данных клиентов с их датой регистрации
    client_registration_dates = {}
    with open(client_filename, mode='r', newline='', encoding='utf-8') as client_file:
        reader = csv.DictReader(client_file)
        for row in reader:
            client_registration_dates[row['ClientID']] = datetime.strptime(row['RegistrationDate'], "%Y-%m-%d %H:%M:%S")
    
    # Чтение данных аккаунтов с привязкой к дате регистрации и валюте
    with open(account_filename, mode='r', newline='', encoding='utf-8') as account_file:
        reader = csv.DictReader(account_file)
        for row in reader:
            accounts.append({
                'AccountID': row['AccountID'],
                'ClientID': row['ClientID'],
                'Balance': float(row['Balance']),  # Считываем баланс аккаунта
                'Currency': row['Currency'],  # Считываем валюту аккаунта
                'RegistrationDate': client_registration_dates.get(row['ClientID'], None)  # Считываем дату регистрации клиента
            })
    return accounts

# Функция для преобразования строки даты в объект datetime
def parse_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S") if date_string else None

# Функция для генерации транзакций на основе ордеров
def generate_transactions_csv(filename, accounts, orders):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Пишем заголовки
        writer.writerow(['TransactionID', 'AccountID', 'TransactionType', 'Amount', 'Currency', 'TransactionDate', 'Status', 'NewBalance'])
        
        for account in accounts:
            # Получаем дату регистрации аккаунта и валюту
            registration_date = account['RegistrationDate']
            currency = account['Currency']  # Используем валюту аккаунта
            
            # Генерация начального депозита после даты регистрации
            initial_deposit = generate_initial_deposit()
            deposit_date = fake.date_time_between(start_date=registration_date, end_date='now').strftime("%Y-%m-%d %H:%M:%S")
            account['Balance'] += initial_deposit  # Добавляем начальный депозит
            writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Deposit', initial_deposit, currency, deposit_date, 'Completed', round(account['Balance'], 2)])

            # Обрабатываем ордера, связанные с аккаунтом
            for order in orders:
                if order['AccountID'] == account['AccountID']:
                    # Преобразуем ExecutionDate в объект datetime
                    execution_date = parse_datetime(order['ExecutionDate'])
                    
                    # Пропускаем ордера без даты выполнения
                    if execution_date is None or execution_date < registration_date:
                        continue  # Пропускаем ордера, которые были до даты регистрации или без ExecutionDate
                    
                    # Снимаем комиссию за ордер
                    commission = order['Commission']
                    account['Balance'] -= commission
                    writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Commission', commission, currency, order['OrderDate'], 'Completed', round(account['Balance'], 2)])
                    
                    # Рассчитываем PnL (прибыль/убыток) по ордеру
                    pnl = generate_trade_pnl()
                    account['Balance'] += pnl
                    writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Profit/Loss', pnl, currency, order['ExecutionDate'], 'Completed', round(account['Balance'], 2)])
                    
                    # Генерируем случайные дополнительные депозиты/снятия
                    if random.random() < 0.3:  # 30% вероятность депозита
                        deposit_amount = generate_initial_deposit() / 10
                        account['Balance'] += deposit_amount
                        deposit_date = fake.date_time_between(start_date=execution_date, end_date='now').strftime("%Y-%m-%d %H:%M:%S")
                        writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Deposit', deposit_amount, currency, deposit_date, 'Completed', round(account['Balance'], 2)])
                    if random.random() < 0.2:  # 20% вероятность снятия
                        withdrawal_amount = min(generate_initial_deposit() / 10, account['Balance'])
                        account['Balance'] -= withdrawal_amount
                        withdrawal_date = fake.date_time_between(start_date=execution_date, end_date='now').strftime("%Y-%m-%d %H:%M:%S")
                        writer.writerow([str(uuid.uuid4()), account['AccountID'], 'Withdrawal', withdrawal_amount, currency, withdrawal_date, 'Completed', round(account['Balance'], 2)])



def generate_transactions(filename, order_filename, account_filename, client_filename):
    # Чтение данных аккаунтов и ордеров
    accounts = read_accounts_and_balances_from_csv(account_filename, client_filename)
    orders = read_orders_from_csv(order_filename)
    # Генерация данных транзакций
    generate_transactions_csv(filename, accounts, orders)