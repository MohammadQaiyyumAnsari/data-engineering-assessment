import csv

def load_snapshot(filepath):
    snapshot = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            snapshot[clean_row['order_id']] = clean_row
    return snapshot

# Snapshot comparison demonstration
prev_snapshot = {
    '1001': {'order_id': '1001', 'status': 'Pending', 'amount': '500'},
    '1002': {'order_id': '1002', 'status': 'Delivered', 'amount': '250'}
}
curr_snapshot = {
    '1001': {'order_id': '1001', 'status': 'Delivered', 'amount': '500'},  # Updated
    '1003': {'order_id': '1003', 'status': 'Delivered', 'amount': '900'}   # Inserted
    # 1002 is Deleted
}

inserted = [rec for k, rec in curr_snapshot.items() if k not in prev_snapshot]
deleted = [rec for k, rec in prev_snapshot.items() if k not in curr_snapshot]
updated = [
    curr_snapshot[k] for k in curr_snapshot 
    if k in prev_snapshot and curr_snapshot[k] != prev_snapshot[k]
]

print(f"Inserted ({len(inserted)}):", inserted)
print(f"Updated  ({len(updated)}):", updated)
print(f"Deleted  ({len(deleted)}):", deleted)