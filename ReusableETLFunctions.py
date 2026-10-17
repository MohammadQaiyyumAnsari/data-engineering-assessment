import csv
from datetime import datetime

def read_csv_data(filepath):
    with open(filepath, mode='r', encoding='utf-8') as f:
        return [{k.strip(): v.strip() for k, v in row.items()} for row in csv.DictReader(f)]

def validate_sales_row(row):
    try:
        qty = int(row['quantity'])
        price = float(row['unit_price'])
        if qty <= 0 or price < 0:
            return False
        return True
    except (ValueError, KeyError):
        return False

def transform_sales_records(records):
    transformed = []
    for r in records:
        if validate_sales_row(r):
            rec = dict(r)
            rec['line_revenue'] = int(r['quantity']) * float(r['unit_price'])
            transformed.append(rec)
    return transformed

def write_csv_data(filepath, data, fieldnames):
    if not data:
        return
    with open(filepath, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Execution test
raw_items = read_csv_data('order_items.csv')
clean_items = transform_sales_records(raw_items)
write_csv_data('cleaned_sales.csv', clean_items, list(clean_items[0].keys()))
print(f"Transformed and wrote {len(clean_items)} records.")