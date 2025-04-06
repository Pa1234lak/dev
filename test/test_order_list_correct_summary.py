import requests

BASE_URL = "https://web-app-cjv8.onrender.com"

def test_order_list_correct():
    session = requests.Session()

    # (Optional) Login if orders page requires authentication
    # response = session.post(f"{BASE_URL}/login", data={"username": "user", "password": "pass"})
    # assert response.status_code in [200, 302]

    # Access the orders page
    response = session.get(f"{BASE_URL}/orders")
    assert response.status_code == 200

    # Check if the response page contains the word "total"
    assert "total" in response.text.lower()
