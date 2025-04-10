import pytest
import requests
from jsonschema import validate
import time

@pytest.fixture
def api_url():
    return "https://api.example.com/customer/"

@pytest.fixture
def headers():
    return {
        "Authorization": "Bearer <JWT token>",
        "Content-Type": "application/json"
    }

@pytest.fixture
def payload():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }

@pytest.fixture
def response_schema():
    return {
        "type": "object",
        "properties": {
            "first_name": {"type": "string"},
            "last_name": {"type": "string"},
            "email": {"type": "string"},
            "dob": {"type": "string", "format": "date-time"},
            "address": {"type": "string"},
            "id": {"type": "string", "format": "uuid"},
            "last_purchase_order_id": {"type": "string", "format": "uuid"},
            "last_activity_time": {"type": "string", "format": "date-time"}
        },
        "required": ["first_name", "last_name", "email", "dob", "address", "id", "last_purchase_order_id", "last_activity_time"]
    }

def test_create_customer(api_url, headers, payload, response_schema):
    start_time = time.time()
    response = requests.post(api_url, json=payload, headers=headers)
    elapsed_time = time.time() - start_time

    # Assert status code
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    # Assert SLA
    assert elapsed_time <= 3, f"SLA exceeded: {elapsed_time}s"

    # Assert response schema
    response_json = response.json()
    validate(instance=response_json, schema=response_schema)

    # Assert data matches payload
    assert response_json["first_name"] == payload["first_name"], "First name mismatch"
    assert response_json["last_name"] == payload["last_name"], "Last name mismatch"
    assert response_json["email"] == payload["email"], "Email mismatch"