import csv
from datetime import datetime

parsed_orders = []

with open('orders.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        raw_date = row['order_date'].strip()
        dt_obj = datetime.strptime(raw_date, '%Y-%m-%d').date()
        parsed_orders.append({
            'order_id': int(row['order_id'].strip()),
            'date_obj': dt_obj,
            'year': dt_obj.year,
            'month': dt_obj.month,
            'day': dt_obj.day
        })

for entry in parsed_orders[:3]:
    print(entry)