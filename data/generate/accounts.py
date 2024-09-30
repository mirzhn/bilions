import csv
import uuid
import random
from faker import Faker

# Инициализируем Faker
fake = Faker()

# Вероятности для типа счета
ACCOUNT_TYPES = ['Real', 'Demo']
ACCOUNT_TYPE_WEIGHTS = [0.8, 0.2]  # 80% реальных счетов, 20% демо-счетов

# Вероятности для валют
CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'AUD']
CURRENCY_WEIGHTS = [0.5, 0.2, 0.1, 0.1, 0.1]  # 50% клиентов используют USD

# Распределение баланса
def generate_balance():
    # 70% клиентов имеют баланс в диапазоне от 1000 до 10,000, 20% — от 10,000 до 50,000, и 10% — больше 50,000
    balance = random.choices(
        [round(random.uniform(1000, 10000), 2),
         round(random.uniform(10000, 50000), 2),
         round(random.uniform(50000, 100000), 2)],
        weights=[0.7, 0.2, 0.1], k=1
    )[0]
    return balance

# Распределение эквити
def generate_equity(balance):
    # Эквити в пределах 80-120% от баланса
    return round(balance * random.uniform(0.8, 1.2), 2)

# Распределение кредитного плеча
LEVERAGES = [1, 10, 25, 50, 100, 200]
LEVERAGE_WEIGHTS = [0.05, 0.15, 0.2, 0.3, 0.2, 0.1]  # 50% клиентов используют плечо до 50

# Функция для генерации типа счета с вероятностями
def generate_account_type():
    return random.choices(ACCOUNT_TYPES, weights=ACCOUNT_TYPE_WEIGHTS, k=1)[0]

# Функция для генерации валюты с вероятностями
def generate_currency():
    return random.choices(CURRENCIES, weights=CURRENCY_WEIGHTS, k=1)[0]

# Функция для генерации кредитного плеча с вероятностями
def generate_leverage():
    return random.choices(LEVERAGES, weights=LEVERAGE_WEIGHTS, k=1)[0]

# Функция для чтения ClientID из файла clients.csv
def read_client_ids_from_csv(filename):
    client_ids = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            client_ids.append(row['ClientID'])  # Считываем ClientID из каждой строки
    return client_ids

# Функция для генерации данных о счетах
def generate_accounts_csv(filename, client_ids):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Пишем заголовки
        writer.writerow(['AccountID', 'ClientID', 'AccountType', 'Currency', 'Balance', 'Equity', 'Leverage'])
        
        for client_id in client_ids:
            # Генерируем случайное количество аккаунтов для каждого клиента (например, от 1 до 3 аккаунтов)
            num_accounts = random.randint(1, 3)
            
            for _ in range(num_accounts):
                account_id = str(uuid.uuid4())  # Генерация уникального UUID для счета
                account_type = generate_account_type()  # Тип счета с вероятностями (реальный или демо)
                currency = generate_currency()  # Валюта счета с вероятностями
                balance = generate_balance()  # Баланс счета с распределением
                equity = generate_equity(balance)  # Эквити на основе баланса
                leverage = generate_leverage()  # Кредитное плечо с вероятностями
                
                # Записываем данные в CSV
                writer.writerow([account_id, client_id, account_type, currency, balance, equity, leverage])

# Генерация данных для аккаунтов
def generate_accounts(filename, client_file_name):
    client_ids = read_client_ids_from_csv(client_file_name)
    generate_accounts_csv(filename, client_ids)

