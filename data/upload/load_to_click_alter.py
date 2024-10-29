import os
import clickhouse_connect
from clickhouse_connect.driver.tools import insert_file

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
    'risk_management': 'risk_management.csv',
    'currency': 'currency.csv'
}

# Создание клиента ClickHouse
client = clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='')

# Цикл по всем таблицам и загрузка данных
for table, csv_file in tables.items():
    csv_path = os.path.join(csv_dir, csv_file)
    
    # Очистка таблицы перед загрузкой
    client.command(f'TRUNCATE TABLE {table}')
    
    # Загрузка данных из CSV с заголовками
    insert_file(client, table, csv_path, fmt='CSVWithNames')
