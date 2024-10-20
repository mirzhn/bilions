
import csv
import uuid
import random
from faker import Faker
from datetime import datetime
fake = Faker()

RISK_LEVEL_DISTRIBUTION = {'Low': 0.4, 'Medium': 0.4, 'High': 0.2}
MAX_LEVERAGE_DISTRIBUTION = {'Low': (10, 30), 'Medium': (50, 100), 'High': (200, 500)}
MARGIN_CALL_LEVEL_DISTRIBUTION = {'Low': (0.8, 1.0), 'Medium': (0.5, 0.8), 'High': (0.3, 0.5)}
STOP_OUT_LEVEL_DISTRIBUTION = {'Low': (0.7, 0.8), 'Medium': (0.4, 0.7), 'High': (0.2, 0.4)}
MAX_DAILY_LOSS_DISTRIBUTION = {'Low': (1000, 5000), 'Medium': (5000, 20000), 'High': (20000, 100000)}
MAX_TRADE_SIZE_DISTRIBUTION = {'Low': (1, 10), 'Medium': (10, 50), 'High': (50, 100)}

def choose_risk_level(account_balance, account_age_days):
    if account_balance > 50000 or account_age_days > 365:
        return 'High'
    if account_balance > 10000 or account_age_days > 180:
        return 'Medium'
    return 'Low'

def generate_max_leverage(risk_level, account_activity_level):
    leverage_range = MAX_LEVERAGE_DISTRIBUTION[risk_level]
    if account_activity_level == 'High':
        return random.randint(leverage_range[1] // 2, leverage_range[1])
    if account_activity_level == 'Medium':
        return random.randint(leverage_range[0], leverage_range[1])
    return random.randint(leverage_range[0], leverage_range[1] // 2)

def assess_account_activity(account_id, trades):
    number_of_trades = trades.get(account_id, 0)
    if number_of_trades > 100:
        return 'High'
    if number_of_trades > 50:
        return 'Medium'
    return 'Low'

def read_account_data_from_csv(filename):
    accounts = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            accounts.append({'AccountID': row['AccountID'], 'Balance': float(row['Balance']), 'RegistrationDate': datetime.strptime(row['RegistrationDate'], '%Y-%m-%d %H:%M:%S')})
        return accounts
        return accounts

def read_order_counts_from_csv(filename):
    order_counts = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            account_id = row['AccountID']
            if account_id in order_counts:
                order_counts[account_id] += 1
            else:
                order_counts[account_id] = 1
        return order_counts
        return order_counts

def read_account_data_from_csv(accounts_filename, clients_filename):
    accounts = []
    client_registration_dates = {}
    with open(clients_filename, mode='r', newline='', encoding='utf-8') as clients_file:
        reader = csv.DictReader(clients_file)
        for row in reader:
            client_registration_dates[row['ClientID']] = datetime.strptime(row['RegistrationDate'], '%Y-%m-%d %H:%M:%S')
    with open(accounts_filename, mode='r', newline='', encoding='utf-8') as accounts_file:
        reader = csv.DictReader(accounts_file)
        for row in reader:
            registration_date = client_registration_dates.get(row['ClientID'], None)
            if registration_date:
                accounts.append({'AccountID': row['AccountID'], 'Balance': float(row['Balance']), 'RegistrationDate': registration_date})
        return accounts
        return accounts

def generate_margin_call_level(risk_level, account_activity_level):
    base_range = MARGIN_CALL_LEVEL_DISTRIBUTION[risk_level]
    if account_activity_level == 'High':
        return round(random.uniform(base_range[0], base_range[1]), 2)
    if account_activity_level == 'Medium':
        return round(random.uniform(base_range[0] * 0.9, base_range[1] * 0.9), 2)
    return round(random.uniform(base_range[0] * 0.8, base_range[1] * 0.8), 2)

def generate_stop_out_level(risk_level, account_activity_level):
    base_range = STOP_OUT_LEVEL_DISTRIBUTION[risk_level]
    if account_activity_level == 'High':
        return round(random.uniform(base_range[0], base_range[1]), 2)
    if account_activity_level == 'Medium':
        return round(random.uniform(base_range[0] * 0.9, base_range[1] * 0.9), 2)
    return round(random.uniform(base_range[0] * 0.8, base_range[1] * 0.8), 2)

def generate_max_daily_loss(risk_level, account_activity_level):
    base_range = MAX_DAILY_LOSS_DISTRIBUTION[risk_level]
    if account_activity_level == 'High':
        return round(random.uniform(base_range[0], base_range[1]), 2)
    if account_activity_level == 'Medium':
        return round(random.uniform(base_range[0] * 0.9, base_range[1] * 0.9), 2)
    return round(random.uniform(base_range[0] * 0.8, base_range[1] * 0.8), 2)

def generate_max_trade_size(risk_level, account_activity_level):
    base_range = MAX_TRADE_SIZE_DISTRIBUTION[risk_level]
    if account_activity_level == 'High':
        return round(random.uniform(base_range[0], base_range[1]), 2)
    if account_activity_level == 'Medium':
        return round(random.uniform(base_range[0] * 0.9, base_range[1] * 0.9), 2)
    return round(random.uniform(base_range[0] * 0.8, base_range[1] * 0.8), 2)

def generate_risk_management_csv(filename, accounts, trades):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['RiskID', 'AccountID', 'MaxLeverage', 'MarginCallLevel', 'StopOutLevel', 'MaxDailyLoss', 'MaxTradeSize', 'RiskLevel', 'CreatedAt', 'UpdatedAt'])
        for account in accounts:
            account_age_days = (datetime.now() - account['RegistrationDate']).days
            risk_level = choose_risk_level(account['Balance'], account_age_days)
            account_activity_level = assess_account_activity(account['AccountID'], trades)
            max_leverage = generate_max_leverage(risk_level, account_activity_level)
            margin_call_level = generate_margin_call_level(risk_level, account_activity_level)
            stop_out_level = generate_stop_out_level(risk_level, account_activity_level)
            max_daily_loss = generate_max_daily_loss(risk_level, account_activity_level)
            max_trade_size = generate_max_trade_size(risk_level, account_activity_level)
            created_at = fake.date_time_between(start_date='-2y', end_date='now')
            updated_at = fake.date_time_between(start_date=created_at, end_date='now')
            writer.writerow([str(uuid.uuid4()), account['AccountID'], max_leverage, margin_call_level, stop_out_level, max_daily_loss, max_trade_size, risk_level, created_at.strftime('%Y-%m-%d %H:%M:%S'), updated_at.strftime('%Y-%m-%d %H:%M:%S')])

def generate_risk_management(filename, accounts_filename, clients_filename, orders_filename):
    accounts = read_account_data_from_csv(accounts_filename, clients_filename)
    order_counts = read_order_counts_from_csv(orders_filename)
    generate_risk_management_csv(filename, accounts, order_counts)