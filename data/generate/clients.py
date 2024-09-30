import csv
import uuid
from faker import Faker
from datetime import datetime, timedelta
import random

# Инициализируем Faker
fake = Faker()

# Вероятности для уровня риска
RISK_LEVELS = ['Low', 'Medium', 'High']
RISK_WEIGHTS = [0.6, 0.3, 0.1]  # 60% - Low, 30% - Medium, 10% - High

# Вероятности для стран
COUNTRIES = ['United States', 'Germany', 'United Kingdom', 'France', 'Canada', 'Australia']
COUNTRY_WEIGHTS = [0.4, 0.2, 0.15, 0.1, 0.1, 0.05]  # 40% из США, 20% из Германии и так далее

# Вероятности для статуса аккаунта
ACCOUNT_STATUSES = ['Active', 'Frozen', 'Closed']
STATUS_WEIGHTS = [0.85, 0.1, 0.05]  # 85% клиентов активны, 10% заморожены, 5% закрыты

# Функция для генерации случайного уровня риска с вероятностями
def generate_risk_level():
    return random.choices(RISK_LEVELS, weights=RISK_WEIGHTS, k=1)[0]

# Функция для генерации страны с вероятностями
def generate_country():
    return random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0]

# Функция для генерации статуса аккаунта с вероятностями
def generate_account_status():
    return random.choices(ACCOUNT_STATUSES, weights=STATUS_WEIGHTS, k=1)[0]

# Функция для генерации даты регистрации с учетом роста числа клиентов по месяцам
def generate_registration_date():
    # Выбираем случайную дату в течение последних 5 лет
    base_date = fake.date_time_between(start_date='-5y', end_date='now')

    # Моделируем рост числа клиентов по месяцам
    months_ago = (datetime.now() - base_date).days // 30  # Примерный возраст клиента в месяцах
    growth_factor = 1 / (months_ago + 1)  # Чем старше клиент, тем меньше его вероятность (чем больше месяцев назад, тем меньше вероятность)
    
    # С увеличением времени увеличиваем вероятность, что дата будет ближе к текущему времени
    return (base_date + timedelta(days=random.random() * growth_factor * 365)).strftime("%Y-%m-%d %H:%M:%S")

# Функция для генерации данных клиентов и сохранения в CSV
def generate_clients_csv(filename, num_records):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Пишем заголовки
        writer.writerow(['ClientID', 'Name', 'Country', 'RegistrationDate', 'AccountStatus', 'RiskLevel'])
        
        for _ in range(num_records):
            client_id = str(uuid.uuid4())  # Генерация уникального UUID
            name = fake.name()  # Генерация случайного имени
            country = generate_country()  # Генерация случайной страны с вероятностью
            registration_date = generate_registration_date()  # Дата регистрации с учетом роста числа клиентов
            account_status = generate_account_status()  # Статус аккаунта с вероятностями
            risk_level = generate_risk_level()  # Уровень риска с вероятностями
            
            # Записываем данные в CSV
            writer.writerow([client_id, name, country, registration_date, account_status, risk_level])

# Генерация данных для 1000 клиентов
def generate_clients(filename, size):
    generate_clients_csv(filename, size)