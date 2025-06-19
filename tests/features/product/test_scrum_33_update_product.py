import requests
import time
from helpers.auth_helper import get_jwt_token, BASE_URL

"""
SCRUM-33 - US - Update Product

Test Objective:
Verify that the /product/{product_id} PUT endpoint:
  - Accepts valid updates to product details.
  - Requires JWT authentication.
  - Returns the updated product in the correct schema.
  - Handles error cases (not found, invalid input, unauthorized) as specified.

Why these tests?
- To confirm the endpoint behaves as expected for valid and invalid scenarios.
- To ensure data integrity, security, and error handling per requirements.
"""

def create_product_for_update(jwt_token):
    """
    Helper to create a product for update tests.
    Ensures the update tests always have a valid product to work with.
    """
    url = f"{BASE_URL}/product/"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "name": "Test Product SCRUM-33",
        "type": "Electronics",
        "created_date": "2023-11-01T00:00:00Z",
        "retail_price": 199.99,
        "remark": "Initial remark"
    }
    resp = requests.post(url, json=payload, headers=headers)
    assert resp.status_code == 200, f"Failed to create product for update: {resp.text}"
    return resp.json()["id"]

def test_scrum_33_update_product():
    """
    Happy path: Valid update.
    - Authenticates as admin.
    - Creates a product, then updates it.
    - Asserts correct response, schema, and performance.
    """
    jwt_token = get_jwt_token()
    product_id = create_product_for_update(jwt_token)

    update_payload = {
        "retail_price": 249.99,
        "remark": "Updated via SCRUM-33"
    }

    url = f"{BASE_URL}/product/{product_id}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Measure response time for SLA compliance
    start_time = time.time()
    response = requests.put(url, json=update_payload, headers=headers)
    response_time = time.time() - start_time

    # Expect 200 OK and updated fields
    assert response.status_code == 200, f"Expected 200, got {response.status_code}, {response.text}"
    data = response.json()
    assert data["id"] == product_id
    assert data["retail_price"] == update_payload["retail_price"]
    assert data["remark"] == update_payload["remark"]

    # Validate ProductOut schema fields
    for key in ["id", "name", "type", "created_date", "retail_price"]:
        assert key in data, f"Missing key {key} in response"

    # Performance check: API should respond within 3 seconds
    assert response_time <= 3, f"Expected response time <= 3s, got {response_time}s"

def test_scrum_33_update_product_not_found():
    """
    Negative case: Try to update a non-existent product.
    - Expects 404 Not Found and correct error schema.
    """
    jwt_token = get_jwt_token()
    fake_id = "00000000-0000-0000-0000-000000000000"
    url = f"{BASE_URL}/product/{fake_id}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {"retail_price": 123.45}
    response = requests.put(url, json=payload, headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data.get("errCode") == 404
    assert "not found" in data.get("errMsg", "").lower()

def test_scrum_33_update_product_invalid_price():
    """
    Negative case: Try to update with invalid price (negative).
    - Expects 400 or 422 error and correct error schema.
    """
    jwt_token = get_jwt_token()
    product_id = create_product_for_update(jwt_token)
    url = f"{BASE_URL}/product/{product_id}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {"retail_price": -10}
    response = requests.put(url, json=payload, headers=headers)
    assert response.status_code in (400, 422)
    data = response.json()
    assert "errCode" in data and "errMsg" in data

def test_scrum_33_update_product_unauthorized():
    """
    Security: Attempt update without JWT.
    - Expects 401 Unauthorized.
    """
    product_id = "00000000-0000-0000-0000-000000000000"
    url = f"{BASE_URL}/product/{product_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {"retail_price": 100}
    response = requests.put(url, json=payload, headers=headers)
    assert response.status_code == 401
