# /tests/features/product/test_post_create_product_missing_name.py
# Helpers
from helpers.auth_helper import get_jwt_token, BASE_URL
import requests
import pytest

'''
  SCRUM-121 - Testcase: [POST] Create Product - Missing Required Field (Name)
  Objective: Verify the API returns an error when the "name" field is missing in the request payload.
  Steps:
    - Send API request with missing "name" field.
  Expected Result:
    - Status code is 400.
    - Response schema should match the defined spec.
    - SLA should <= 3s.
'''
@pytest.mark.api
@pytest.mark.product
def test_scrum_121_post_create_product_missing_name():

    # Precondition: Retrieve a valid JWT token
    jwt_token = get_jwt_token()

    # Endpoint and headers
    url = f"{BASE_URL}/product/"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    # Request payload with missing "name" field
    payload = {
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }

    # Send API request with missing "name" field
    response = requests.post(url, headers=headers, json=payload)

    # Validate status code is 400
    assert response.status_code == 400, f"Expected status code 400 but got {response.status_code}"

    # Validate response schema matches the defined spec
    response_json = response.json()
    assert response_json.get("errorCode") == "400", f"Expected errorCode '400' but got {response_json.get('errorCode')}"
    assert response_json.get("errorMsg") == "Field 'name' is required.", f"Expected errorMsg 'Field \"name\" is required.' but got {response_json.get('errorMsg')}"

    # Validate SLA is <= 3s
    assert response.elapsed.total_seconds() <= 3, f"SLA exceeded: {response.elapsed.total_seconds()}s"