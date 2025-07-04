import pytest
import requests
import time

@pytest.mark.api
def test_scrum_120_create_product_valid_input(db_check_product_exists, get_auth_token, api_base_url):
    """
    SCRUM-120: [POST] Create Product - Valid Input

    Objective:
        Verify the API response status, schema, SLA, and database entry when creating a product with valid input.
    """
    url = f"{api_base_url}/product/"
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
    elapsed = time.time() - start_time

    # SLA check
    assert elapsed <= 3, f"SLA exceeded: {elapsed}s"

    # Status code check
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Response schema check
    data = response.json()
    assert "id" in data and isinstance(data["id"], str)
    assert data["name"] == payload["name"]
    assert data["type"] == payload["type"]
    assert data["retail_price"] == payload["retail_price"]
    assert data["creation_date"] == payload["creation_date"]

    # Database check (assumes db_check_product_exists is a fixture/helper)
    assert db_check_product_exists(data["id"]), "Product not found in database"
