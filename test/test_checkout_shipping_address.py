import requests
import re

BASE_URL = "https://web-app-cjv8.onrender.com"

def test_checkout_shipping_address():
    session = requests.Session()

    # Step 1: Add item to cart (assuming you can't checkout without items)
    add_response = session.post(f"{BASE_URL}/cart/add", data={"product_id": 1, "quantity": 1})
    assert add_response.status_code in (200, 302), "Failed to add item to cart"

    # Step 2: Access the checkout page to extract CSRF token if needed
    checkout_page = session.get(f"{BASE_URL}/checkout")
    assert checkout_page.status_code == 200

    csrf_token = None
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', checkout_page.text)
    if match:
        csrf_token = match.group(1)

    # Step 3: Submit the shipping form
    shipping_data = {
        "address": "123 Street Name",
        "city": "Bangalore",
        "zip": "560001",
        "continue": "Continue"
    }

    if csrf_token:
        shipping_data["csrfmiddlewaretoken"] = csrf_token

    headers = {}
    if csrf_token:
        headers["Referer"] = f"{BASE_URL}/checkout"

    shipping_response = session.post(f"{BASE_URL}/checkout", data=shipping_data, headers=headers)
    assert shipping_response.status_code in (200, 302), f"Shipping POST failed: {shipping_response.status_code}"

    # Step 4: Verify if redirected to payment step
    assert "payment" in shipping_response.text.lower()
