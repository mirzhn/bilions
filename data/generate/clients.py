
import csv
import uuid
from faker import Faker
from datetime import datetime, timedelta
import random
import numpy as np
import pycountry

fake = Faker()
RISK_LEVELS = ['Low', 'Medium', 'High']
RISK_WEIGHTS = [0.6, 0.3, 0.1]
COUNTRIES = [country.name for country in pycountry.countries]
COUNTRY_WEIGHTS = []
for country in COUNTRIES:
    if country in ['United States', 'Germany', 'United Kingdom', 'France', 'Canada', 'Australia']:
        COUNTRY_WEIGHTS.append(0.02)
    else:
        COUNTRY_WEIGHTS.append(0.005)
total_weight = sum(COUNTRY_WEIGHTS)
COUNTRY_WEIGHTS = [weight / total_weight for weight in COUNTRY_WEIGHTS]
ACCOUNT_STATUSES = ['Active', 'Frozen', 'Closed']
STATUS_WEIGHTS = [0.85, 0.1, 0.05]

def generate_risk_level():
    return random.choices(RISK_LEVELS, weights=RISK_WEIGHTS, k=1)[0]

def generate_country():
    return random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0]

def generate_account_status():
    return random.choices(ACCOUNT_STATUSES, weights=STATUS_WEIGHTS, k=1)[0]

def generate_registration_date():
    current_date = datetime.now()
    start_date = current_date - timedelta(days=1825)
    days_since_start = np.random.exponential(scale=547.5)
    registration_date = start_date + timedelta(days=min(days_since_start, (current_date - start_date).days))
    if registration_date > current_date:
        registration_date = current_date - timedelta(days=random.randint(1, 7))
    return registration_date.strftime('%Y-%m-%d %H:%M:%S')

def generate_clients_csv(filename, num_records):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ClientID', 'Name', 'Country', 'RegistrationDate', 'AccountStatus', 'RiskLevel'])
        for _ in range(num_records):
            client_id = str(uuid.uuid4())
            name = fake.name()
            country = generate_country()
            registration_date = generate_registration_date()
            account_status = generate_account_status()
            risk_level = generate_risk_level()
            writer.writerow([client_id, name, country, registration_date, account_status, risk_level])

def generate_clients(filename, size):
    generate_clients_csv(filename, size)