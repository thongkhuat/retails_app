import requests
import json
import time

'''
  SCRUM-120 - Verify the API response status, schema, SLA, and database entry when creating a product with valid input
  Objective: Ensure that the product creation API works as expected with valid input.
  Steps:
    1. Send API request with valid data.
  Expected Result:
    * Status code is 201.
    * Response schema should match the defined spec.
    * SLA should <= 3s.
    * Product is successfully created in the database.
'''
import pytest

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

    # Step 1: Send API request with valid data
    start_time = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    elapsed_time = time.time() - start_time

    # Validate status code is 201
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"

    # Validate response schema matches the defined spec
    expected_schema = {
        "id": str,
        "name": "Smartphone",
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }
    response_json = response.json()
    assert isinstance(response_json["id"], str), "Response 'id' should be a string"
    assert response_json["name"] == expected_schema["name"], "Response 'name' does not match"
    assert response_json["type"] == expected_schema["type"], "Response 'type' does not match"
    assert response_json["retail_price"] == expected_schema["retail_price"], "Response 'retail_price' does not match"
    assert response_json["creation_date"] == expected_schema["creation_date"], "Response 'creation_date' does not match"

    # Validate SLA is <= 3s
    assert elapsed_time <= 3, f"API response time exceeded SLA: {elapsed_time}s"

    # Validate product is successfully created in the database
    # (This step assumes a function `is_product_in_database` exists to verify the database entry)
    # Example: assert is_product_in_database(response_json["id"]), "Product not found in database"