import requests
import time

# Helpers
from helpers.auth_helper import get_jwt_token, BASE_URL

'''
  Objective: Verify the authentication method
  Steps:
    1. Send API request with valid credential.
  Expected Result:
    - Status code is 200.
    - SLA should <= 3s.
'''
def test_login_by_valid_credential():

    # Endpoint and headers
    url = f"{BASE_URL}/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Request data
    data = {"username": "admin", "password": "12345678"}

    # Step 1: Send API request with invalid "retail_price" value
    start_time = time.time()
    response = requests.post(url, data=data, headers=headers)
    response_time = time.time() - start_time

    # Validate status code is 200
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Validate SLA <= 3s
    assert response_time <= 3, f"Expected response time <= 3s, got {response_time}s"