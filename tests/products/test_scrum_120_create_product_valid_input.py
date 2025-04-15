# tests/products/test_scrum_120_create_product_valid_input.py
import requests
import time

# Helpers
from ..helpers.auth_helper import get_jwt_token

'''
  SCRUM-120 - Testcase: [POST] Create Product - Valid Input
  Objective: Verify the API response status, schema, SLA, and database entry when creating a product with valid input.
  Steps:
    # Send API request with valid data.
  Expected Result:
    * Status code is 201.
    * Response schema should match the defined spec.
    * SLA should <= 3s.
    * Product is successfully created in the database.
'''
def test_scrum_120_create_product_valid_input():

    # Precondition: Retrieve a valid JWT token
    jwt_token = get_jwt_token()

    # Endpoint and headers
    url = "http://localhost:8000/product/"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    # Request payload
    payload = {
        "name": "Smartphone",
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }

    # Step: Send API request with valid data
    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    response_time = time.time() - start_time

    # Validate status code is 201
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"

    # Validate response schema matches the defined spec
    response_json = response.json()
    assert response_json.get("id"), "Response schema missing 'id' field."
    assert response_json.get("name") == "Smartphone", f"Expected name 'Smartphone', got {response_json.get('name')}"
    assert response_json.get("type") == "Electronics", f"Expected type 'Electronics', got {response_json.get('type')}"
    assert response_json.get("retail_price") == 699.99, f"Expected retail_price 699.99, got {response_json.get('retail_price')}"
    assert response_json.get("creation_date") == "2023-10-01T00:00:00Z", f"Expected creation_date '2023-10-01T00:00:00Z', got {response_json.get('creation_date')}"

    # Validate SLA <= 3s
    assert response_time <= 3, f"Expected response time <= 3s, got {response_time}s"

    # Validate product is successfully created in the database (mocked database validation example)
    # Note: Replace with actual database validation logic if available
    assert response_json.get("id") is not None, "Expected product ID to be present in the response."