import csv
from datetime import datetime

dq_issues = []

# Validate incremental orders file
with open('orders_incremental.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for line_num, row in enumerate(reader, start=2):
        row = {k.strip(): v.strip() for k, v in row.items()}
        
        # Missing / Empty Customer ID
        if not row.get('customer_id'):
            dq_issues.append((line_num, row['order_id'], 'MISSING_CUSTOMER_ID', row))
            
        # Invalid Date Format
        try:
            datetime.strptime(row['order_date'], '%Y-%m-%d')
        except (ValueError, KeyError):
            dq_issues.append((line_num, row['order_id'], 'INVALID_DATE', row))

# Validate order items file
with open('order_items.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for line_num, row in enumerate(reader, start=2):
        row = {k.strip(): v.strip() for k, v in row.items()}
        try:
            qty = int(row['quantity'])
            price = float(row['unit_price'])
            if qty <= 0:
                dq_issues.append((line_num, row['order_item_id'], 'NEGATIVE_OR_ZERO_QUANTITY', row))
            if price < 0:
                dq_issues.append((line_num, row['order_item_id'], 'NEGATIVE_PRICE', row))
        except ValueError:
            dq_issues.append((line_num, row['order_item_id'], 'NON_NUMERIC_METRIC', row))

print(f"Total DQ issues detected: {len(dq_issues)}")
for issue in dq_issues:
    print(f"Line {issue[0]} | Record Key {issue[1]} | Rule: {issue[2]}")