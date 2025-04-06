import requests

BASE_URL = "https://web-app-cjv8.onrender.com"

def test_user_registration():
    session = requests.Session()

    # Simulate registration POST request
    response = session.post(f"{BASE_URL}/register", data={
        "username": "newuser123",
        "email": "newuser123@example.com",
        "password1": "Password@123",
        "password2": "Password@123",
        "register": "Register"
    })

    # Accept 200 OK or 302 Redirect
    assert response.status_code in [200, 302]

    # Check if 'email' is in the redirected or resulting page
    page = session.get(f"{BASE_URL}/")
    assert "email" in page.text.lower()
