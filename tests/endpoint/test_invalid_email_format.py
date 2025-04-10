import pytest
import requests

@pytest.mark.api
def test_invalid_email_format():
    # Setup
    url = "http://api.example.com/customer/"
    headers = {
        "Authorization": "Bearer <JWT token>",
        "Content-Type": "application/json"
    }
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email-format"
    }

    # Send API request
    response = requests.post(url, json=payload, headers=headers)

    # Assertions
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    response_json = response.json()
    assert "errorCode" in response_json and response_json["errorCode"] == "400", "Error code mismatch"
    assert "errorMsg" in response_json and response_json["errorMsg"] == "Invalid email format", "Error message mismatch"
    assert response.elapsed.total_seconds() <= 3, f"SLA exceeded: {response.elapsed.total_seconds()}s"