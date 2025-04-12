# tests/test_create_product.py
import requests
import json
import time

'''
  SCRUM-110 - Verify the API successfully creates a product with valid details
  Objective: Verify the API successfully creates a product with valid details.
  Steps:
    # Send API request with valid data.
  Expected Result:
    * Status code is 201.
    * Response schema should match the defined spec.
    * SLA should <= 3s.
    * Data should match the payload input.
'''
@pytest.mark.api
def test_scrum_110_create_product():
    # Endpoint and headers
    url = "http://testdomain/product/"
    headers = {
        "Authorization": "Bearer <JWT token>",
        "Content-Type": "application/json"
    }

    # Request payload
    payload = {
        "name": "Laptop",
        "type": "Electronics",
        "retail_price": 1200.00,
        "creation_date": "2023-10-01T10:00:00Z"
    }

    # Send API request with valid data
    start_time = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    elapsed_time = time.time() - start_time

    # Validate status code is 201
    assert response.status_code == 201

    # Validate response schema matches the defined spec
    response_data = response.json()
    assert "name" in response_data and response_data["name"] == payload["name"]
    assert "type" in response_data and response_data["type"] == payload["type"]
    assert "retail_price" in response_data and response_data["retail_price"] == payload["retail_price"]
    assert "creation_date" in response_data and response_data["creation_date"] == payload["creation_date"]
    assert "id" in response_data and isinstance(response_data["id"], str)

    # Validate SLA should <= 3s
    assert elapsed_time <= 3

    # Validate data matches the payload input
    assert response_data["name"] == payload["name"]
    assert response_data["type"] == payload["type"]
    assert response_data["retail_price"] == payload["retail_price"]
    assert response_data["creation_date"] == payload["creation_date"]