import pytest

def calculate_revenue(quantity, unit_price):
    if quantity < 0 or unit_price < 0:
        raise ValueError("Metrics must be non-negative")
    return quantity * unit_price

def is_valid_customer_id(customer_id):
    return customer_id is not None and str(customer_id).strip() != ""

def find_duplicates(keys):
    seen = set()
    dups = set()
    for k in keys:
        if k in seen:
            dups.add(k)
        seen.add(k)
    return dups

# Pytest Test Cases
def test_calculate_revenue_valid():
    assert calculate_revenue(3, 2500.0) == 7500.0
    assert calculate_revenue(0, 100.0) == 0.0

def test_calculate_revenue_negative_input():
    with pytest.raises(ValueError):
        calculate_revenue(-1, 50.0)
    with pytest.raises(ValueError):
        calculate_revenue(5, -10.0)

def test_is_valid_customer_id():
    assert is_valid_customer_id("101") is True
    assert is_valid_customer_id("") is False
    assert is_valid_customer_id(None) is False
    assert is_valid_customer_id("   ") is False

def test_find_duplicates():
    order_ids = [1001, 1002, 1002, 1016, 1018, 1018]
    assert find_duplicates(order_ids) == {1002, 1018}