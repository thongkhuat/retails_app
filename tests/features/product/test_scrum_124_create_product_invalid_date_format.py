import requests
import time
from helpers.auth_helper import get_jwt_token, BASE_URL

'''
  SCRUM-124 - Testcase: [POST] Create Product - Invalid Date Format
  Objective: Verify that the API returns an error when the "creation_date" field contains an invalid date format.
  Steps:
    1. Send API request with invalid "creation_date" format.
  Expected Result:
    - Status code is 400.
    - Response schema should match the defined spec.
    - SLA should <= 3s.
'''
def test_scrum_124_create_product_invalid_date_format():

    # Precondition: Retrieve a valid JWT token
    jwt_token = get_jwt_token()

    # Endpoint and headers
    url = f"{BASE_URL}/product/"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    # Test data
    payload = {
        "name": "Smartphone",
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "01-10-2023"
    }

    # Step 1: Send API request with invalid "creation_date" format
    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    elapsed_time = time.time() - start_time

    # Validate status code is 400
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    # Validate response schema
    response_json = response.json()
    assert response_json.get("errorCode") == "400", f"Expected errorCode '400', got {response_json.get('errorCode')}"
    assert response_json.get("errorMsg") == "Field 'creation_date' must be in ISO 8601 format.", \
        f"Expected errorMsg 'Field 'creation_date' must be in ISO 8601 format.', got {response_json.get('errorMsg')}"

    # Validate SLA <= 3s
    assert elapsed_time <= 3, f"SLA exceeded: {elapsed_time}s (Expected <= 3s)"