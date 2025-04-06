import requests
import re

BASE_URL = "https://web-app-cjv8.onrender.com"

def test_checkout_payment_success():
    session = requests.Session()

    # Step 1: Add item to cart first (or login if needed)
    add_response = session.post(
        f"{BASE_URL}/cart/add",
        data={
            "product_id": 1,
            "quantity": 1
        }
    )
    assert add_response.status_code in (200, 302), "Failed to add item to cart"

    # Step 2: Access checkout page (to get CSRF or session data if needed)
    checkout_page = session.get(f"{BASE_URL}/checkout")
    assert checkout_page.status_code == 200

    # Optional: Extract CSRF token if required (assuming Django-style)
    csrf_token = None
    match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', checkout_page.text)
    if match:
        csrf_token = match.group(1)

    # Step 3: Simulate payment
    payment_data = {
        "card_number": "4242424242424242",
        "expiry": "12/26",
        "cvv": "123",
        "pay": "Pay"
    }

    if csrf_token:
        payment_data["csrfmiddlewaretoken"] = csrf_token

    headers = {}
    if csrf_token:
        headers["Referer"] = f"{BASE_URL}/checkout"

    pay_response = session.post(f"{BASE_URL}/checkout", data=payment_data, headers=headers)
    assert pay_response.status_code in (200, 302), f"Payment POST failed: {pay_response.status_code}"

    # Step 4: Confirm success message
    assert "payment successful" in pay_response.text.lower()
