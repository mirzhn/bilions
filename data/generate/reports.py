import csv
import uuid
import random
from faker import Faker
from datetime import datetime, timedelta
import json

# Initialize Faker
fake = Faker()

# Define report types with probabilities
REPORT_TYPES = ['Trade Report', 'PnL Report', 'Position Report']
REPORT_TYPE_WEIGHTS = [0.5, 0.3, 0.2]  # 50% for Trade Report, 30% for PnL Report, 20% for Position Report

# Define report statuses with probabilities
REPORT_STATUSES = ['Generated', 'Sent']
REPORT_STATUS_WEIGHTS = [0.7, 0.3]  # 70% chance of 'Generated', 30% chance of 'Sent'

# Define delivery methods with probabilities
DELIVERY_METHODS = ['Email', 'API', 'Internal System']
DELIVERY_METHOD_WEIGHTS = [0.6, 0.3, 0.1]  # 60% Email, 30% API, 10% Internal System

# Example report data (in JSON format)
def generate_report_data(report_type):
    if report_type == 'Trade Report':
        return {
            "total_trades": random.randint(5, 20),
            "total_volume": round(random.uniform(10000, 50000), 2),
            "total_commission": round(random.uniform(50, 500), 2)
        }
    elif report_type == 'PnL Report':
        return {
            "total_pnl": round(random.uniform(-10000, 20000), 2),
            "total_revenue": round(random.uniform(10000, 50000), 2),
            "total_costs": round(random.uniform(5000, 15000), 2)
        }
    else:  # Position Report
        return {
            "open_positions": random.randint(1, 10),
            "closed_positions": random.randint(1, 10),
            "average_position_size": round(random.uniform(1000, 5000), 2)
        }

# Function to read account data and client registration date from CSV
def read_account_and_client_data(account_filename, client_filename):
    account_data = []
    client_registration_dates = {}

    # Read client registration dates
    with open(client_filename, mode='r', newline='', encoding='utf-8') as client_file:
        reader = csv.DictReader(client_file)
        for row in reader:
            client_registration_dates[row['ClientID']] = datetime.strptime(row['RegistrationDate'], "%Y-%m-%d %H:%M:%S")

    # Read account data and match with client registration date
    with open(account_filename, mode='r', newline='', encoding='utf-8') as account_file:
        reader = csv.DictReader(account_file)
        for row in reader:
            account_data.append({
                'AccountID': row['AccountID'],
                'ClientID': row['ClientID'],
                'RegistrationDate': client_registration_dates[row['ClientID']]  # Assign registration date from clients.csv
            })

    return account_data

# Function to generate report data
def generate_reports_csv(filename, account_data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['ReportID', 'AccountID', 'ReportType', 'GeneratedDate', 'ReportPeriodStart', 'ReportPeriodEnd', 'Status', 'DeliveryMethod', 'ReportData'])

        for account in account_data:
            # Choose random report type based on weighted probabilities
            report_type = random.choices(REPORT_TYPES, weights=REPORT_TYPE_WEIGHTS, k=1)[0]

            # Generate report dates within the registration date constraint
            registration_date = account['RegistrationDate']
            generated_date = fake.date_time_between(start_date=registration_date, end_date='now')
            report_period_start = generated_date - timedelta(days=random.randint(7, 30))  # Report period start (7 to 30 days before generation date)
            report_period_end = generated_date  # End of the report period is the generation date

            # Choose random status and delivery method based on weighted probabilities
            status = random.choices(REPORT_STATUSES, weights=REPORT_STATUS_WEIGHTS, k=1)[0]
            delivery_method = random.choices(DELIVERY_METHODS, weights=DELIVERY_METHOD_WEIGHTS, k=1)[0]

            # Generate report data
            report_data = generate_report_data(report_type)
            report_data_json = json.dumps(report_data)  # Convert report data to JSON

            # Write row to CSV
            writer.writerow([
                str(uuid.uuid4()),  # ReportID
                account['AccountID'],  # AccountID
                report_type,  # ReportType
                generated_date.strftime("%Y-%m-%d %H:%M:%S"),  # GeneratedDate
                report_period_start.strftime("%Y-%m-%d %H:%M:%S"),  # ReportPeriodStart
                report_period_end.strftime("%Y-%m-%d %H:%M:%S"),  # ReportPeriodEnd
                status,  # Status
                delivery_method,  # DeliveryMethod
                report_data_json  # ReportData
            ])


def generate_reports(filename, clients_filename, accounts_filename):
    account_data = read_account_and_client_data(accounts_filename, clients_filename)
    # Generate report data
    generate_reports_csv(filename, account_data)