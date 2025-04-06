import pytest
import requests

BASE_URL = "https://web-app-cjv8.onrender.com"

@pytest.fixture
def session():
    return requests.Session()

def test_add_item_with_quantity(session):
    response = session.post(f"{BASE_URL}/cart/add", data={"product_id": 1})
    assert response.status_code == 200

    response = session.post(f"{BASE_URL}/cart/update", data={"product_id": 1, "quantity": 3})
    assert response.status_code == 200