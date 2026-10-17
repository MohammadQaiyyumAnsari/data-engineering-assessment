import csv
from datetime import datetime

def run_end_to_end_etl(input_file, clean_output_file, error_report_file):
    valid_records = []
    error_records = []
    seen_keys = {}

    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for line_num, row in enumerate(reader, start=2):
            row = {k.strip(): v.strip() for k, v in row.items()}
            order_id = row.get('order_id')
            cust_id = row.get('customer_id')
            order_date = row.get('order_date')
            errors = []

            # Check 1: Mandatory Customer ID
            if not cust_id:
                errors.append("MISSING_CUSTOMER_ID")

            # Check 2: Valid Date Format
            try:
                datetime.strptime(order_date, '%Y-%m-%d')
            except (ValueError, TypeError):
                errors.append("INVALID_ORDER_DATE")

            # Check 3: Business Key & Deduplication Tracking
            try:
                row_ts = datetime.strptime(row['updated_at'], '%Y-%m-%d %H:%M:%S')
            except (ValueError, KeyError):
                row_ts = datetime.min

            if errors:
                for err in errors:
                    error_records.append({
                        'line_number': line_num,
                        'order_id': order_id,
                        'error_type': err,
                        'raw_data': str(row)
                    })
            else:
                # Deduplication logic: Keep latest updated_at
                if order_id in seen_keys:
                    prev_ts, prev_idx = seen_keys[order_id]
                    if row_ts > prev_ts:
                        # Quarantine superseded version as duplicate
                        error_records.append({
                            'line_number': line_num,
                            'order_id': order_id,
                            'error_type': 'SUPERSEDED_DUPLICATE_VERSION',
                            'raw_data': str(valid_records[prev_idx])
                        })
                        valid_records[prev_idx] = row
                        seen_keys[order_id] = (row_ts, prev_idx)
                    else:
                        error_records.append({
                            'line_number': line_num,
                            'order_id': order_id,
                            'error_type': 'DUPLICATE_IGNORED',
                            'raw_data': str(row)
                        })
                else:
                    seen_keys[order_id] = (row_ts, len(valid_records))
                    valid_records.append(row)

    # Write clean output
    if valid_records:
        headers = ['order_id', 'customer_id', 'order_date', 'order_status', 'payment_method', 'updated_at']
        with open(clean_output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(valid_records)

    # Write error quarantine report
    if error_records:
        error_headers = ['line_number', 'order_id', 'error_type', 'raw_data']
        with open(error_report_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=error_headers)
            writer.writeheader()
            writer.writerows(error_records)

    print(f"ETL Complete: {len(valid_records)} Clean Records | {len(error_records)} Quarantined Records")

# Run on the Section A incremental data
if __name__ == '__main__':
    run_end_to_end_etl(
        input_file='orders_incremental.csv',
        clean_output_file='clean_orders.csv',
        error_report_file='error_report.csv'
    )