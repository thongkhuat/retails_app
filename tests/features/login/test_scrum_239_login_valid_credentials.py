import requests
import time

from helpers.auth_helper import BASE_URL

'''
SCRUM-239 - Testcase: [POST] Login valid credentials
Objective: Verify successful JWT token generation with valid username and password.
Steps:
  1. Send POST request to /login with valid credentials.
Expected Result:
  - Status code is 200.
  - Response contains a valid JWT token and token_type "bearer".
  - SLA should <= 3s.
'''

def test_scrum_239_login_valid_credentials():
    url = f"{BASE_URL}/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": "admin",
        "password": "12345678"
    }

    start_time = time.time()
    response = requests.post(url, data=data, headers=headers)
    response_time = time.time() - start_time

    # Validate status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Validate response time (SLA)
    assert response_time <= 3, f"Expected response time <= 3s, got {response_time}s"

    # Validate response schema and values
    response_json = response.json()
    assert "access_token" in response_json and isinstance(response_json["access_token"], str) and response_json["access_token"], \
        "Response must contain a non-empty 'access_token' string"
    assert response_json.get("token_type") == "bearer", f"Expected token_type 'bearer', got {response_json.get('token_type')}"