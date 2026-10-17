import csv
from collections import defaultdict

product_revenue = defaultdict(float)

with open('order_items.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pid = row['product_id'].strip()
        qty = int(row['quantity'].strip())
        price = float(row['unit_price'].strip())
        product_revenue[pid] += qty * price

for pid, rev in sorted(product_revenue.items(), key=lambda x: x[1], reverse=True):
    print(f"Product: {pid:<6} | Total Revenue: {rev:>10,.2f}")