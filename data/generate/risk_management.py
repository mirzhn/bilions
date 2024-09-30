import csv
import uuid
import random
from faker import Faker
from datetime import datetime

# Инициализация Faker
fake = Faker()

# Настройки вероятностей распределений уровней риска
RISK_LEVEL_DISTRIBUTION = {
    'Low': 0.4,      # 40% вероятность
    'Medium': 0.4,   # 40% вероятность
    'High': 0.2      # 20% вероятность
}

# Настройки распределений для MaxLeverage по уровням риска
MAX_LEVERAGE_DISTRIBUTION = {
    'Low': [10, 20, 30],
    'Medium': [50, 100],
    'High': [200, 300, 500]
}

# Настройки распределений для MarginCallLevel по уровням риска
MARGIN_CALL_LEVEL_DISTRIBUTION = {
    'Low': (0.8, 1.0),     # 80-100%
    'Medium': (0.5, 0.8),  # 50-80%
    'High': (0.3, 0.5)     # 30-50%
}

# Настройки распределений для StopOutLevel по уровням риска
STOP_OUT_LEVEL_DISTRIBUTION = {
    'Low': (0.7, 0.8),     # 70-80%
    'Medium': (0.4, 0.7),  # 40-70%
    'High': (0.2, 0.4)     # 20-40%
}

# Настройки распределений для MaxDailyLoss по уровням риска
MAX_DAILY_LOSS_DISTRIBUTION = {
    'Low': (1000, 5000),      # от $1000 до $5000
    'Medium': (5000, 20000),  # от $5000 до $20000
    'High': (20000, 100000)   # от $20000 до $100000
}

# Настройки распределений для MaxTradeSize по уровням риска
MAX_TRADE_SIZE_DISTRIBUTION = {
    'Low': (1, 10),      # от 1 до 10 лотов
    'Medium': (10, 50),  # от 10 до 50 лотов
    'High': (50, 100)    # от 50 до 100 лотов
}

# Функция для выбора случайного уровня риска на основе настроек вероятности
def choose_risk_level():
    return random.choices(list(RISK_LEVEL_DISTRIBUTION.keys()), weights=RISK_LEVEL_DISTRIBUTION.values(), k=1)[0]

# Функция для генерации максимального кредитного плеча на основе уровня риска
def generate_max_leverage(risk_level):
    return random.choice(MAX_LEVERAGE_DISTRIBUTION[risk_level])

# Функция для генерации уровня Margin Call на основе уровня риска
def generate_margin_call_level(risk_level):
    return round(random.uniform(*MARGIN_CALL_LEVEL_DISTRIBUTION[risk_level]), 2)

# Функция для генерации уровня Stop Out на основе уровня риска
def generate_stop_out_level(risk_level):
    return round(random.uniform(*STOP_OUT_LEVEL_DISTRIBUTION[risk_level]), 2)

# Функция для генерации максимальных потерь в день на основе уровня риска
def generate_max_daily_loss(risk_level):
    return round(random.uniform(*MAX_DAILY_LOSS_DISTRIBUTION[risk_level]), 2)

# Функция для генерации максимального размера сделки на основе уровня риска
def generate_max_trade_size(risk_level):
    return round(random.uniform(*MAX_TRADE_SIZE_DISTRIBUTION[risk_level]), 2)

# Функция для чтения данных аккаунтов из файла accounts.csv
def read_account_ids_from_csv(filename):
    account_ids = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            account_ids.append(row['AccountID'])  # Считываем AccountID из каждой строки
    return account_ids

# Функция для генерации данных по управлению рисками
def generate_risk_management_csv(filename, account_ids):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Пишем заголовки
        writer.writerow(['RiskID', 'AccountID', 'MaxLeverage', 'MarginCallLevel', 'StopOutLevel', 'MaxDailyLoss', 'MaxTradeSize', 'RiskLevel', 'CreatedAt', 'UpdatedAt'])
        
        for account_id in account_ids:
            # Генерация уровня риска для каждого аккаунта
            risk_level = choose_risk_level()
            
            # Генерация параметров управления рисками на основе уровня риска
            max_leverage = generate_max_leverage(risk_level)
            margin_call_level = generate_margin_call_level(risk_level)
            stop_out_level = generate_stop_out_level(risk_level)
            max_daily_loss = generate_max_daily_loss(risk_level)
            max_trade_size = generate_max_trade_size(risk_level)
            
            # Временные метки для создания и обновления записей
            created_at = fake.date_time_between(start_date='-2y', end_date='now')  # создаем объект datetime
            updated_at = fake.date_time_between(start_date=created_at, end_date='now')  # используем объект datetime
            
            # Записываем данные в CSV
            writer.writerow([
                str(uuid.uuid4()),  # RiskID
                account_id,  # AccountID
                max_leverage,  # MaxLeverage
                margin_call_level,  # MarginCallLevel
                stop_out_level,  # StopOutLevel
                max_daily_loss,  # MaxDailyLoss
                max_trade_size,  # MaxTradeSize
                risk_level,  # RiskLevel
                created_at.strftime("%Y-%m-%d %H:%M:%S"),  # Преобразуем в строку
                updated_at.strftime("%Y-%m-%d %H:%M:%S")  # Преобразуем в строку
            ])


def generate_risk_management(filename, accounts_filename):
    # Чтение данных аккаунтов из файла accounts.csv
    account_ids = read_account_ids_from_csv(accounts_filename)
    # Генерация данных для управления рисками
    generate_risk_management_csv(filename, account_ids)