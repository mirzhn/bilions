import csv
import uuid
import random
from faker import Faker
from datetime import datetime

fake = Faker()
COMMISSION_TYPES = ['Fixed', 'Dynamic', 'Percentage', 'Tiered', 'Flat']
COMMISSION_WEIGHTS = [0.5, 0.2, 0.15, 0.1, 0.05]

def generate_commission_type():
    return random.choices(COMMISSION_TYPES, weights=COMMISSION_WEIGHTS, k=1)[0]

def read_commission_transactions_from_csv(filename):
    transactions = []
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['TransactionType'] == 'Commission':
                transactions.append({'TransactionID': row['TransactionID'], 'AccountID': row['AccountID'], 'Amount': float(row['Amount']), 'Currency': row['Currency'], 'TransactionDate': row['TransactionDate'], 'TradeID': row['TradeID'] if 'TradeID' in row else None})
        return transactions

def generate_commissions_csv(filename, transactions):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CommissionID', 'TradeID', 'AccountID', 'CommissionType', 'CommissionAmount', 'CommissionDate'])
        for transaction in transactions:
            commission_type = generate_commission_type()
            writer.writerow([str(uuid.uuid4()), transaction['TradeID'] if transaction['TradeID'] else str(uuid.uuid4()), transaction['AccountID'], commission_type, transaction['Amount'], transaction['TransactionDate']])

def generate_commissions(filename, transactions_filename):
    transactions = read_commission_transactions_from_csv(transactions_filename)
    generate_commissions_csv(filename, transactions)