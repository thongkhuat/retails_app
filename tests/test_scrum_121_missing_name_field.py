# tests/test_scrum_121_missing_name_field.py
import requests
import time

'''
  SCRUM-121 - Verify the API returns an error when the "name" field is missing in the request payload
  Objective: Ensure the API returns a 400 error and appropriate error message when the "name" field is missing in the request payload.
  Steps:
    1. Send an API request with the payload missing the "name" field.
  Expected Result:
    - Status code is 400.
    - Response schema matches the defined specification.
    - SLA is ≤ 3 seconds.
'''
import pytest

@pytest.mark.api
def test_scrum_121_missing_name_field():
    # Endpoint and headers
    url = "http://testdomain/product/"
    headers = {
        "Authorization": "Bearer <JWT token>",
        "Content-Type": "application/json"
    }

    # Request payload missing the "name" field
    payload = {
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }

    # Step 1: Send an API request with the payload missing the "name" field
    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    response_time = time.time() - start_time

    # Validate status code is 400
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    # Validate response schema matches the defined specification
    response_json = response.json()
    assert "errorCode" in response_json, "Response is missing 'errorCode'"
    assert "errorMsg" in response_json, "Response is missing 'errorMsg'"
    assert response_json["errorCode"] == "400", f"Expected errorCode '400', got {response_json['errorCode']}"
    assert response_json["errorMsg"] == "Field 'name' is required.", f"Expected errorMsg 'Field 'name' is required.', got {response_json['errorMsg']}"

    # Validate SLA is ≤ 3 seconds
    assert response_time <= 3, f"Response time exceeded SLA: {response_time} seconds"