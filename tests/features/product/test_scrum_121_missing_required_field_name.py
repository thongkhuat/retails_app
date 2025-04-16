import requests
import pytest
from helpers.auth_helper import get_jwt_token, BASE_URL

'''
  SCRUM-121 - Testcase: [POST] Create Product - Missing Required Field (Name)
  Objective: Verify the API returns an error when the "name" field is missing in the request payload.
  Steps:
    1. Send API request with missing "name" field.
  Expected Result:
    - Status code is 400.
    - Response schema should match the defined spec.
    - SLA should <= 3s.
'''
@pytest.mark.api
@pytest.mark.negative
def test_scrum_121_missing_required_field_name():

    # Precondition: Retrieve a valid JWT token
    jwt_token = get_jwt_token()

    # Endpoint and headers
    url = f"{BASE_URL}/product/"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    # Payload with missing "name" field
    payload = {
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }

    # Step 1: Send API request with missing "name" field
    response = requests.post(url, headers=headers, json=payload)

    # Validate status code
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"

    # Validate response schema
    response_json = response.json()
    assert response_json.get("errorCode") == "400", f"Expected errorCode '400', got {response_json.get('errorCode')}"
    assert response_json.get("errorMsg") == "Field 'name' is required.", f"Expected errorMsg 'Field 'name' is required.', got {response_json.get('errorMsg')}"

    # Validate SLA (response time <= 3 seconds)
    assert response.elapsed.total_seconds() <= 3, f"SLA exceeded: {response.elapsed.total_seconds()}s"