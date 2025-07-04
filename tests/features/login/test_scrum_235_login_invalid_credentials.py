import requests
import time

from helpers.auth_helper import BASE_URL

'''
  SCRUM-235 - Testcase: [POST] Login invalid credentials
  Objective: Verify login returns 401 error with incorrect username or password.
  Steps:
    1. Send POST request to /login with invalid password.
  Expected Result:
    - Status code is 401.
    - Response matches error schema with errCode 401.
'''

def test_scrum_235_login_invalid_credentials():
    # Endpoint and headers
    url = f"{BASE_URL}/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Request data
    data = {
        "username": "admin",
        "password": "wrongpassword"
    }

    # Step 1: Send API request with invalid credentials
    start_time = time.time()
    response = requests.post(url, data=data, headers=headers)
    response_time = time.time() - start_time

    # Validate status code is 401
    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"

    # Validate error response schema
    response_json = response.json()
    assert response_json.get("errCode") == 401, f"Expected errCode 401, got {response_json.get('errCode')}"
    assert response_json.get("errMsg") == "Incorrect username or password", \
        f"Expected errMsg 'Incorrect username or password', got {response_json.get('errMsg')}"

    # Validate SLA <= 3s
    assert response_time <= 3, f"Expected response time <= 3s, got {response_time}s"
