import pytest
import requests
import time

@pytest.mark.api
def test_update_user_account_user_not_found():
    """
    SCRUM-183: [PUT] Update User Account Details - User Not Found

    Objective:
        Verify the API returns not found error when userId does not exist.

    Endpoint:
        PUT /api/users/{userid}/account

    Preconditions:
        - API service is running.
        - Valid authentication token.

    Test Data:
        userid: 99999 (non-existent)
        email: newemail@example.com

    Expected:
        - Status code is 404.
        - Response body: {"status": "error", "message": "User not found"}
        - SLA <= 3s
    """
    base_url = "http://localhost:8000"  # Adjust as needed
    userid = 99999
    url = f"{base_url}/api/users/{userid}/account"
    headers = {
        "Authorization": "Bearer <JWT token>",  # Replace with a valid token
        "Content-Type": "application/json"
    }
    payload = {
        "email": "newemail@example.com"
    }

    start_time = time.time()
    response = requests.put(url, json=payload, headers=headers)
    elapsed_time = time.time() - start_time

    assert response.status_code == 404, f"Expected 404, got {response.status_code}"
    response_json = response.json()
    assert response_json.get("status") == "error", f"Expected status 'error', got {response_json.get('status')}"
    assert response_json.get("message") == "User not found", f"Expected message 'User not found', got {response_json.get('message')}"
    assert elapsed_time <= 3, f"API response time exceeded SLA: {elapsed_time:.2f}s"
