import requests

from helpers.auth_helper import BASE_URL

def test_scrum_234_login_valid_credentials():
    """
    SCRUM-234: [POST] Login valid credentials
    Objective: Verify login returns JWT token with correct username and password.
    """

    url = f"{BASE_URL}/login"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "username": "admin",
        "password": "12345678"
    }

    response = requests.post(url, data=data, headers=headers)

    # Assert status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Assert response body
    resp_json = response.json()
    assert "access_token" in resp_json, "access_token not in response"
    assert resp_json["access_token"], "access_token is empty"
    assert resp_json.get("token_type") == "bearer", f"token_type is {resp_json.get('token_type')}, expected 'bearer'"
