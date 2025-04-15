import requests
import pytest
import time

'''
  SCRUM-123 - Testcase: [POST] Create Product - Unauthorized Access
  Objective: Verify the API returns an error when the request is made without authentication.
  Steps:
    1. Send API request without an authentication token.
  Expected Result:
    - Status code is 401.
    - Response schema should match the defined spec.
    - SLA should be ≤ 3 seconds.
'''
@pytest.mark.api
@pytest.mark.products
def test_scrum_123_create_product_unauthorized():

    # Endpoint and headers
    url = "http://localhost:8000/product/"
    headers = {
        "Content-Type": "application/json"
    }

    # Request payload
    payload = {
        "name": "Smartphone",
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }

    # Measure SLA start time
    start_time = time.time()

    # Step: Send API request without an authentication token
    response = requests.post(url, headers=headers, json=payload)

    # Validate status code is 401
    assert response.status_code == 401, f"Expected status code 401 but got {response.status_code}"

    # Validate response schema
    response_data = response.json()
    assert response_data.get("errorCode") == "401", f"Expected errorCode '401' but got {response_data.get('errorCode')}"
    assert response_data.get("errorMsg") == "Authentication required.", f"Expected errorMsg 'Authentication required.' but got {response_data.get('errorMsg')}"

    # Validate SLA ≤ 3 seconds
    elapsed_time = time.time() - start_time
    assert elapsed_time <= 3, f"SLA exceeded: {elapsed_time} seconds"