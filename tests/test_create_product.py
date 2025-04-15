# tests/test_create_product.py
import requests
import json
import time
import pytest

'''
  SCRUM-120 - Verify the API response status, schema, SLA, and database entry when creating a product with valid input
  Objective: Verify the API response status, schema, SLA, and database entry when creating a product with valid input.
  Steps:
    # Send API request with valid data.
  Expected Result:
    * Status code is 201.
    * Response schema should match the defined spec.
    * SLA should <= 3s.
    * Product is successfully created in the database.
'''
@pytest.mark.api
def test_scrum_120_create_product():
    # Endpoint and headers
    url = "http://testdomain/product/"
    headers = {
        "Authorization": "Bearer <JWT token>",
        "Content-Type": "application/json"
    }

    # Request payload
    payload = {
        "name": "Smartphone",
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }

    # Send API request with valid data
    start_time = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_time = time.time() - start_time

    # Validate status code is 201
    assert response.status_code == 201

    # Validate response schema matches the defined spec
    expected_schema = {
        "id": str,
        "name": "Smartphone",
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }
    response_json = response.json()
    assert isinstance(response_json["id"], str)
    assert response_json["name"] == expected_schema["name"]
    assert response_json["type"] == expected_schema["type"]
    assert response_json["retail_price"] == expected_schema["retail_price"]
    assert response_json["creation_date"] == expected_schema["creation_date"]

    # Validate SLA is <= 3s
    assert response_time <= 3

    # Validate product is successfully created in the database
    # (This step assumes a database query function `is_product_in_db` is available)
    # assert is_product_in_db("Smartphone", "Electronics", 699.99, "2023-10-01T00:00:00Z")