import csv

customers_dict = {}

with open('customers.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Strip trailing/leading spaces from keys and values
        clean_row = {k.strip(): v.strip() for k, v in row.items()}
        cust_id = int(clean_row['customer_id'])
        customers_dict[cust_id] = {
            'customer_name': clean_row['customer_name'],
            'country': clean_row['country'],
            'city': clean_row['city'],
            'signup_date': clean_row['signup_date']
        }

print(f"Loaded {len(customers_dict)} customers.")
print("Sample record (101):", customers_dict[101])