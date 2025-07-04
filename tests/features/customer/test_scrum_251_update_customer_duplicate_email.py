import requests
import uuid

from helpers.auth_helper import get_jwt_token, BASE_URL

"""
SCRUM-251 - [PUT] Update customer with duplicate email
Objective: Verify response is 400 Bad Request when updating email to one already used by another customer.
"""

def create_customer(jwt_token, email):
    url = f"{BASE_URL}/customer/"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": email,
        "password": "testpass123"
    }
    resp = requests.post(url, json=payload, headers=headers)
    assert resp.status_code == 200, f"Failed to create customer: {resp.text}"
    return resp.json()["id"]

def test_scrum_251_update_customer_duplicate_email():
    # Step 1: Get admin JWT token
    jwt_token = get_jwt_token()

    # Step 2: Create two customers with different emails
    email1 = f"testuser_{uuid.uuid4()}@example.com"
    email2 = f"dupemail_{uuid.uuid4()}@example.com"
    customer_id_1 = create_customer(jwt_token, email1)
    customer_id_2 = create_customer(jwt_token, email2)

    # Step 3: Attempt to update customer 2's email to email1 (duplicate)
    url = f"{BASE_URL}/customer/{customer_id_2}"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "email": email1
    }

    response = requests.put(url, json=payload, headers=headers)

    # Step 4: Assert status code is 400
    assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"

    # Step 5: Assert error schema
    resp_json = response.json()
    assert resp_json.get("errCode") == 400, f"Expected errCode 400, got {resp_json.get('errCode')}"
    assert resp_json.get("errMsg") in ["Duplicate email", "Email already exists"], \
        f"Expected errMsg 'Duplicate email' or 'Email already exists', got {resp_json.get('errMsg')}"
