import requests
import uuid

from helpers.auth_helper import get_jwt_token, BASE_URL

"""
SCRUM-250 - [PUT] Update customer with invalid payload (missing required fields)
Objective: Verify response is 400 Bad Request when payload is missing required fields or contains invalid structure.
"""

def get_existing_customer_id(jwt_token):
    # Create a valid customer to get a valid customer_id for testing
    url = f"{BASE_URL}/customer/"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": f"test_{uuid.uuid4()}@example.com",
        "password": "testpass123"
    }
    resp = requests.post(url, json=payload, headers=headers)
    assert resp.status_code == 200, f"Setup failed: {resp.text}"
    return resp.json()["id"]

def test_scrum_250_update_customer_invalid_payload():
    # Step 1: Get admin JWT token
    jwt_token = get_jwt_token()

    # Step 2: Get a valid customer_id
    customer_id = get_existing_customer_id(jwt_token)

    # Step 3: Prepare invalid payload and headers
    url = f"{BASE_URL}/customer/{customer_id}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    invalid_payload = {
        "unknown_field": "value"
    }

    # Step 4: Send PUT request with invalid payload
    response = requests.put(url, json=invalid_payload, headers=headers)

    # Step 5: Assert status code is 400
    assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"

    # Step 6: Assert error schema
    resp_json = response.json()
    assert resp_json.get("errCode") == 400, f"Expected errCode 400, got {resp_json.get('errCode')}"
    assert resp_json.get("errMsg") == "Invalid payload", f"Expected errMsg 'Invalid payload', got {resp_json.get('errMsg')}"