import requests

BASE_URL = "https://web-app-cjv8.onrender.com"

def test_order_tracking_dashboard():
    session = requests.Session()

    # (Optional) Login if dashboard is protected
    # login_response = session.post(f"{BASE_URL}/login", data={"username": "user", "password": "pass"})
    # assert login_response.status_code in [200, 302]

    # Access the dashboard page
    dashboard_response = session.get(f"{BASE_URL}/dashboard")
    assert dashboard_response.status_code == 200

    # Optional: Parse link to "Track Order" if needed (we're assuming static path here)
    # Simulate clicking "Track Order" link
    track_response = session.get(f"{BASE_URL}/dashboard/track")  # Adjust path if needed
    assert track_response.status_code == 200

    # Check if the content has "order status"
    assert "order status" in track_response.text.lower()
