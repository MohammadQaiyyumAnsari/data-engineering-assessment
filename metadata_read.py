import csv

files = ['customers.csv', 'products.csv', 'orders.csv', 'order_items.csv']

for file_path in files:
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = [col.strip() for col in next(reader)]
        row_count = sum(1 for _ in reader)
        print(f"File: {file_path:<16} | Rows: {row_count:<3} | Columns: {headers}")