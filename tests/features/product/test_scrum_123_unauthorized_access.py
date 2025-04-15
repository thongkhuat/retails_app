import requests
import pytest
import time

# Helpers
from helpers.auth_helper import BASE_URL

'''
  SCRUM-123 - Testcase: [POST] Create Product - Unauthorized Access
  Objective: Verify the API returns an error when the request is made without authentication.
  Steps:
    # Send API request without authentication token.
  Expected Result:
    * Status code is 401.
    * Response schema should match the defined spec.
    * SLA should <= 3s.
'''
@pytest.mark.unauthorized
@pytest.mark.api
def test_scrum_123_unauthorized_access():
    # Endpoint and headers
    url = f"{BASE_URL}/product/"
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

    # Measure start time for SLA validation
    start_time = time.time()

    # Send API request without authentication token
    response = requests.post(url, json=payload, headers=headers)

    # Measure end time and calculate SLA
    elapsed_time = time.time() - start_time

    # Validate status code
    assert response.status_code == 401, f"Expected status code 401, but got {response.status_code}"

    # Validate response schema
    response_json = response.json()
    assert "errorCode" in response_json and response_json["errorCode"] == "401", "Error code mismatch"
    assert "errorMsg" in response_json and response_json["errorMsg"] == "Authentication required.", "Error message mismatch"

    # Validate SLA
    assert elapsed_time <= 3, f"SLA exceeded: {elapsed_time} seconds"