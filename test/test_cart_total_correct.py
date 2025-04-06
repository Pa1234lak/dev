import requests
import re

BASE_URL = "https://web-app-cjv8.onrender.com"

def test_cart_total_correct():
    session = requests.Session()

    # Add an item to the cart
    add_response = session.post(f"{BASE_URL}/cart/add", data={"product_id": 1})
    assert add_response.status_code == 200 or add_response.status_code == 302  # Some apps redirect after post

    # Access the cart page
    cart_response = session.get(f"{BASE_URL}/cart")
    assert cart_response.status_code == 200

    # Try to find ₹ symbol and extract total
    match = re.search(r'₹\s*([\d\.]+)', cart_response.text)
    assert match, "No ₹ symbol or total found in response"

    total = float(match.group(1))
    assert total > 0, f"Expected total > 0 but got {total}"
