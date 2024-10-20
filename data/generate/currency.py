import csv
from datetime import datetime, timedelta
import random
import os

def read_currencies_from_accounts(filename):
    currencies = set()
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            currencies.add(row['Currency'])
    return list(currencies)

# Функция для генерации данных по курсам валют с использованием случайных значений
def generate_currency_rates_csv(filename, currencies, base_currency='USD'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Пишем заголовки
        writer.writerow(['Date', 'BaseCurrency', 'TargetCurrency', 'ExchangeRate'])
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5 * 365)
        
        # Генерируем данные по всем валютам за каждый день в течение 5 лет
        current_date = start_date
        while current_date <= end_date:
            current_date_str = current_date.strftime("%Y-%m-%d")
            for target_currency in currencies:
                if target_currency != base_currency:
                    exchange_rate = round(random.uniform(0.5, 1.5), 4)  # Генерация случайного курса валют
                    writer.writerow([current_date_str, base_currency, target_currency, exchange_rate])
            current_date += timedelta(days=1)

# Функция для запуска генерации данных по курсам валют
def generate_currency_rates(filename, accounts_filename):
    # Чтение валют из файла accounts.csv
    currencies = read_currencies_from_accounts(accounts_filename)
    # Генерация данных по курсам валют и запись в файл
    generate_currency_rates_csv(filename, currencies)

# Пример использования
generate_currency_rates('./out/currency.csv', './out/accounts.csv')
