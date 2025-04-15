import requests
import pytest
import time
from helpers.auth_helper import get_jwt_token

'''
  SCRUM-121 - Testcase: [POST] Create Product - Missing Required Field (Name)
  Objective: Verify the API returns an error when the "name" field is missing in the request payload.
  Steps:
    1. Fetch JWT token as a precondition.
    2. Send API request with missing "name" field.
  Expected Result:
    - Status code is 400.
    - Response schema should match the defined spec.
    - SLA should <= 3s.
'''
@pytest.mark.api
def test_scrum_121_create_product_missing_name():
    # Base URL and credentials
    base_url = "http://testdomain"
    username = "admin"
    password = "12345678"

    # Fetch JWT token
    token = get_jwt_token(base_url, username, password)

    # Endpoint and headers
    url = f"{base_url}/product/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Request payload
    payload = {
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }

    # Step 1: Send API request with missing "name" field
    start_time = time.time()
    response = requests.post(url, headers=headers, json=payload)
    elapsed_time = time.time() - start_time

    # Validate status code is 400
    assert response.status_code == 400

    # Validate response schema matches the defined spec
    response_json = response.json()
    assert response_json["errorCode"] == "400"
    assert response_json["errorMsg"] == "Field 'name' is required."

    # Validate SLA is <= 3s
    assert elapsed_time <= 3