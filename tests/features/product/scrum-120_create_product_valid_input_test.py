import pytest
import requests
import time

@pytest.mark.api
def test_create_product_valid_input(db_client, get_auth_token):
    """
    SCRUM-120: [POST] Create Product - Valid Input
    Objective: Verify the API response status, schema, SLA, and database entry when creating a product with valid input.
    """
    url = "http://localhost:8000/product/"
    payload = {
        "name": "Smartphone",
        "type": "Electronics",
        "retail_price": 699.99,
        "creation_date": "2023-10-01T00:00:00Z"
    }
    headers = {
        "Authorization": f"Bearer {get_auth_token()}",
        "Content-Type": "application/json"
    }

    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    elapsed_time = time.time() - start_time

    # Assert status code
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Assert SLA
    assert elapsed_time <= 3, f"SLA exceeded: {elapsed_time:.2f}s"

    # Assert response schema
    data = response.json()
    assert "id" in data and isinstance(data["id"], str)
    assert data["name"] == payload["name"]
    assert data["type"] == payload["type"]
    assert data["retail_price"] == payload["retail_price"]
    assert data["creation_date"] == payload["creation_date"]

    # Assert product is created in the database
    db_product = db_client.get_product_by_id(data["id"])
    assert db_product is not None, "Product not found in database"
    assert db_product["name"] == payload["name"]
    assert db_product["type"] == payload["type"]
    assert db_product["retail_price"] == payload["retail_price"]
    assert db_product["creation_date"] == payload["creation_date"]
