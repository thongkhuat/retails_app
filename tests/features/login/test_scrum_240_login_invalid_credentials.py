import requests
import time

from helpers.auth_helper import BASE_URL

'''
  SCRUM-240 - Testcase: [POST] Login invalid credentials
  Objective: Verify 401 Unauthorized response for invalid login credentials without JWT token.
  Steps:
    1. Send POST request to /login with invalid credentials.
  Expected Result:
    - Status code is 401.
    - Response matches error schema.
    - SLA should <= 3s.
'''
def test_scrum_240_login_invalid_credentials():
    # Endpoint and headers
    url = f"{BASE_URL}/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Request data (invalid credentials)
    data = {
        "username": "admin",
        "password": "wrongpassword"
    }

    # Step 1: Send POST request with invalid credentials
    start_time = time.time()
    response = requests.post(url, data=data, headers=headers)
    response_time = time.time() - start_time

    # Validate status code is 401
    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"

    # Validate response schema
    response_json = response.json()
    assert response_json.get("errCode") == 401, f"Expected errCode 401, got {response_json.get('errCode')}"
    assert response_json.get("errMsg") == "Incorrect username or password", \
        f"Expected errMsg 'Incorrect username or password', got {response_json.get('errMsg')}"

    # Validate SLA <= 3s
    assert response_time <= 3, f"Expected response time <= 3s, got {response_time}s"
