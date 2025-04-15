import requests
import time

# Helpers
from helpers.auth_helper import get_jwt_token, BASE_URL

'''
  SCRUM-122 - Testcase: [POST] Create Product - Invalid Retail Price
  Objective: Verify the API returns an error when the "retail_price" field contains an invalid value.
  Steps:
    1. Send API request with invalid "retail_price" value.
  Expected Result:
    - Status code is 400.
    - Response schema should match the defined spec.
    - SLA should <= 3s.
'''
def test_scrum_122_create_product_invalid_retail_price():

    # Precondition: Retrieve a valid JWT token
    jwt_token = get_jwt_token()

    # Endpoint and headers
    url = f"{BASE_URL}/product/"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Request payload
    payload = {
        "name": "Smartphone",
        "type": "Electronics",
        "retail_price": -50,
        "creation_date": "2023-10-01T00:00:00Z",
        "remark": "string"
    }

    # Step 1: Send API request with invalid "retail_price" value
    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    response_time = time.time() - start_time

    # Validate status code is 400
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    # Validate response schema
    response_json = response.json()
    assert response_json.get("errorCode") == "400", f"Expected errorCode '400', got {response_json.get('errorCode')}"
    assert response_json.get("errorMsg") == "Field 'retail_price' must be a positive number.", \
        f"Expected errorMsg 'Field 'retail_price' must be a positive number.', got {response_json.get('errorMsg')}"

    # Validate SLA <= 3s
    assert response_time <= 3, f"Expected response time <= 3s, got {response_time}s"