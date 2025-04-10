import requests
import pytest

@pytest.mark.customers
def test_unauthorized_request():
    # Endpoint and headers
    url = "http://api.example.com/customer/"
    headers = {
        "Content-Type": "application/json"
    }

    # Request payload
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }

    # Send POST request without authentication token
    response = requests.post(url, json=payload, headers=headers)

    # Assert status code
    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"

    # Assert response schema
    response_json = response.json()
    assert "errorCode" in response_json, "Response missing 'errorCode'"
    assert "errorMsg" in response_json, "Response missing 'errorMsg'"
    assert response_json["errorCode"] == "401", f"Expected errorCode '401', got {response_json['errorCode']}"
    assert response_json["errorMsg"] == "Unauthorized access", f"Expected errorMsg 'Unauthorized access', got {response_json['errorMsg']}"

    # Assert SLA
    assert response.elapsed.total_seconds() <= 3, f"Response time exceeded SLA: {response.elapsed.total_seconds()}s"