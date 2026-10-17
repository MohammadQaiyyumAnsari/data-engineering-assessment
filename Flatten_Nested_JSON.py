import json

sample_nested_json = """
[
  {
    "order_id": 1001,
    "order_date": "2025-01-05",
    "customer": {
      "customer_id": 101,
      "name": "Alice",
      "address": {"city": "Hyderabad", "country": "India"}
    },
    "items": [
      {"product_id": "P101", "qty": 1, "price": 75000},
      {"product_id": "P103", "qty": 2, "price": 2500}
    ]
  }
]
"""

nested_data = json.loads(sample_nested_json)
flattened_records = []

for order in nested_data:
    cust = order.get("customer", {})
    addr = cust.get("address", {})
    for item in order.get("items", []):
        flattened_records.append({
            "order_id": order.get("order_id"),
            "order_date": order.get("order_date"),
            "customer_id": cust.get("customer_id"),
            "customer_name": cust.get("name"),
            "city": addr.get("city"),
            "country": addr.get("country"),
            "product_id": item.get("product_id"),
            "quantity": item.get("qty"),
            "unit_price": item.get("price"),
            "line_total": item.get("qty") * item.get("price")
        })

print("Flattened rows count:", len(flattened_records))
print("Sample row:", flattened_records[0])