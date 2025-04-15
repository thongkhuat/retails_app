# /tests/features/product/test_scrum_121_missing_name.py
import requests
import time
from helpers.auth_helper import get_jwt_token, BASE_URL

'''
  SCRUM-121 - Testcase: [POST] Create Product - Missing Required Field (Name)
  Objective: Verify the API returns an error when the "name" field is missing in the request payload.
  Steps:
    1. Send an API request with the missing "name" field.
  Expected Result:
    - Status code should be 400.
    - Response schema should match the defined specification.
    - SLA should be ≤ 3 seconds.
'''
def test_scrum_121_missing_name():

    # Precondition: Retrieve a valid JWT token
    jwt_token = get_jwt_token()

    # Endpoint and headers
    url = f"{BASE_URL}/product/"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    # Request payload
    payload = {
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }

    # Measure response time and send the request
    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    response_time = time.time() - start_time

    # Validate status code
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    # Validate response schema
    response_json = response.json()
    assert response_json.get("errorCode") == "400", f"Expected errorCode '400', got {response_json.get('errorCode')}"
    assert response_json.get("errorMsg") == "Field 'name' is required.", f"Expected errorMsg 'Field 'name' is required.', got {response_json.get('errorMsg')}"

    # Validate SLA
    assert response_time <= 3, f"Expected response time ≤ 3 seconds, got {response_time} seconds"