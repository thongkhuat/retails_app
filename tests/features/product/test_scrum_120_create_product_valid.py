import requests
import time

# Helpers
from helpers.auth_helper import get_jwt_token, BASE_URL

'''
  SCRUM-120 - Testcase: [POST] Create Product - Valid Input
  Objective: Verify the API response status, schema, SLA, and database entry when creating a product with valid input.
  Steps:
    1. Send API request with valid data.
    2. Validate response status, schema, SLA.
    3. Verify product is created in the database by fetching with returned id.
  Expected Result:
    - Status code is 201.
    - Response schema should match the defined spec.
    - SLA should <= 3s.
    - Product is successfully created in the database.
'''

def test_scrum_120_create_product_valid():
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
        "retail_price": 699.99,
        "created_date": "2023-10-01T00:00:00Z"
    }

    # Step 1: Send API request with valid data
    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    response_time = time.time() - start_time

    # Validate status code is 201
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"

    # Validate response schema
    response_json = response.json()
    assert "id" in response_json, "Response missing 'id'"
    assert response_json["name"] == payload["name"], f"Expected name '{payload['name']}', got '{response_json['name']}'"
    assert response_json["type"] == payload["type"], f"Expected type '{payload['type']}', got '{response_json['type']}'"
    assert response_json["retail_price"] == payload["retail_price"], f"Expected retail_price '{payload['retail_price']}', got '{response_json['retail_price']}'"
    assert response_json["created_date"] == payload["created_date"], f"Expected created_date '{payload['created_date']}', got '{response_json['created_date']}'"

    # Validate SLA <= 3s
    assert response_time <= 3, f"Expected response time <= 3s, got {response_time}s"

    # Step 2: Verify product is created in the database by fetching with returned id
    product_id = response_json["id"]
    get_url = f"{BASE_URL}/product/{product_id}"
    get_headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json"
    }
    get_response = requests.get(get_url, headers=get_headers)
    assert get_response.status_code == 200, f"Expected GET status code 200, got {get_response.status_code}"
    get_json = get_response.json()
    assert get_json["id"] == product_id, "Fetched product id does not match"
    assert get_json["name"] == payload["name"], "Fetched product name does not match"
    assert get_json["type"] == payload["type"], "Fetched product type does not match"
    assert get_json["retail_price"] == payload["retail_price"], "Fetched product retail_price does not match"
    assert get_json["created_date"] == payload["created_date"], "Fetched product created_date does not match"
