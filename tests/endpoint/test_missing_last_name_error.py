import pytest
import requests

@pytest.mark.api
def test_missing_last_name_error():
    # Setup
    url = "https://api.example.com/customer/"
    headers = {
        "Authorization": "Bearer <JWT token>",
        "Content-Type": "application/json"
    }
    payload = {
        "first_name": "John",
        "email": "john.doe@example.com"
    }
    
    # Send API request
    response = requests.post(url, json=payload, headers=headers)
    
    # Assertions
    assert response.status_code == 400, f"Expected status code 400, got {response.status_code}"
    response_json = response.json()
    assert response_json.get("errorCode") == "400", f"Expected errorCode '400', got {response_json.get('errorCode')}"
    assert response_json.get("errorMsg") == "Last name is required", f"Expected errorMsg 'Last name is required', got {response_json.get('errorMsg')}"
    assert response.elapsed.total_seconds() <= 3, f"Expected SLA <= 3s, got {response.elapsed.total_seconds()}s"