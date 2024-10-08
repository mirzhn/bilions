import os
import subprocess

# Путь к директории с CSV-файлами
csv_dir = './out/'

# Список таблиц и соответствующих CSV-файлов
tables = {
    'clients': 'clients.csv',
    'accounts': 'accounts.csv',
    'orders': 'orders.csv',
    'trades': 'trades.csv',
    'transactions': 'transactions.csv',
    'commissions': 'commissions.csv',
    'reports': 'reports.csv', 
    'risk_management': 'risk_management.csv'
}

# Цикл по всем таблицам и загрузка данных
for table, csv_file in tables.items():
    csv_path = os.path.join(csv_dir, csv_file)
    cmd = f"clickhouse-client --port 9000 --user default --query='INSERT INTO {table} FORMAT CSV' < {csv_path}"
    subprocess.run(cmd, shell=True)
