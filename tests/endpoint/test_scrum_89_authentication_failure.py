import requests
import pytest

@pytest.mark.performance
@pytest.mark.authentication
def test_authentication_via_oauth2():
    # Endpoint and headers
    url = "http://api.example.com/customer/"
    headers = {
        "Content-Type": "application/json"
    }

    # Send GET request without authentication token
    response = requests.get(url, headers=headers)

    # Validate status code
    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"

    # Validate response schema
    expected_schema = {
        "errorCode": "401",
        "errorMsg": "Invalid token"
    }
    assert response.json() == expected_schema, f"Response schema mismatch. Expected {expected_schema}, got {response.json()}"

    # Validate SLA
    assert response.elapsed.total_seconds() <= 3, f"SLA exceeded. Response time: {response.elapsed.total_seconds()} seconds"