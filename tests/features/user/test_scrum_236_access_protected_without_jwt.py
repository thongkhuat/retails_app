import requests
import time

from helpers.auth_helper import BASE_URL

'''
  SCRUM-236 - Testcase: [POST] Access protected endpoint without JWT token
  Objective: Verify 401 error is returned when JWT token is missing.
  Steps:
    1. Send POST request to /user without Authorization header.
  Expected Result:
    - Status code is 401.
    - Response matches error schema with errCode 401 and errMsg "Not authenticated".
    - SLA should <= 3s.
'''

def test_scrum_236_access_protected_without_jwt():
    # Endpoint and headers
    url = f"{BASE_URL}/user"
    headers = {
        "Content-Type": "application/json"
    }

    # Request data
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }

    # Step 1: Send API request without Authorization header
    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    response_time = time.time() - start_time

    # Validate status code is 401
    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"

    # Validate error response schema
    response_json = response.json()
    assert response_json.get("errCode") == 401, f"Expected errCode 401, got {response_json.get('errCode')}"
    assert response_json.get("errMsg") == "Not authenticated", \
        f"Expected errMsg 'Not authenticated', got {response_json.get('errMsg')}"

    # Validate SLA <= 3s
    assert response_time <= 3, f"Expected response time <= 3s, got {response_time}s"
