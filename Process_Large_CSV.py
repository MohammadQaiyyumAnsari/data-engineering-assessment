import csv

def process_csv_in_chunks(file_path, chunk_size=5):
    """Generator yielding chunks of rows from a CSV file."""
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        chunk = []
        for row in reader:
            chunk.append(row)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

total_revenue = 0.0
for batch in process_csv_in_chunks('order_items.csv', chunk_size=5):
    batch_revenue = sum(int(r['quantity'].strip()) * float(r['unit_price'].strip()) for r in batch)
    total_revenue += batch_revenue

print(f"Total Revenue computed in chunks: {total_revenue:,.2f}")