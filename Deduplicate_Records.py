import csv
from datetime import datetime

deduped_orders = {}

with open('orders_incremental.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row = {k.strip(): v.strip() for k, v in row.items()}
        order_id = row['order_id']
        
        try:
            current_ts = datetime.strptime(row['updated_at'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            current_ts = datetime.min

        if order_id not in deduped_orders or current_ts > deduped_orders[order_id]['_parsed_ts']:
            row['_parsed_ts'] = current_ts
            deduped_orders[order_id] = row

# Write deduped clean output
with open('orders_incremental_deduped.csv', mode='w', newline='', encoding='utf-8') as f:
    fieldnames = ['order_id', 'customer_id', 'order_date', 'order_status', 'payment_method', 'updated_at']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for record in deduped_orders.values():
        record.pop('_parsed_ts', None)
        writer.writerow(record)

print(f"Unique orders saved: {len(deduped_orders)}")