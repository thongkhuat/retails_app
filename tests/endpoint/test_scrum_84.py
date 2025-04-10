import pytest
import requests

@pytest.fixture
def base_url():
    return "http://api.example.com"

@pytest.fixture
def headers():
    return {
        "Authorization": "Bearer <JWT token>",
        "Content-Type": "application/json"
    }

@pytest.fixture
def invalid_payload():
    return {
        "price": "invalid_price",
        "availability": "yes",
        "remarks": 12345
    }

@pytest.fixture
def product_id():
    return 12345

def test_validate_error_handling_for_payload_schema_mismatches(base_url, headers, invalid_payload, product_id):
    url = f"{base_url}/product/{product_id}"
    response = requests.put(url, json=invalid_payload, headers=headers)

    # Assert status code
    assert response.status_code == 400

    # Assert response schema
    response_json = response.json()
    assert "errorCode" in response_json
    assert "errorMsg" in response_json
    assert response_json["errorCode"] == "400"
    assert response_json["errorMsg"] == "Invalid request payload"