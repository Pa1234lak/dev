import requests

BASE_URL = "https://web-app-cjv8.onrender.com"

def test_user_login():
    session = requests.Session()

    # Simulate login POST request
    login_response = session.post(f"{BASE_URL}/login", data={
        "username": "newuser123",
        "password": "Password@123"
    })

    # Accept both 200 OK or 302 Redirect
    assert login_response.status_code in [200, 302]

    # Now access dashboard or home page to verify login success
    dashboard_response = session.get(f"{BASE_URL}/dashboard")
    assert dashboard_response.status_code == 200
    assert "dashboard" in dashboard_response.text.lower()
