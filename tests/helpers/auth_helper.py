# tests/helpers/auth_helper.py
import requests

BASE_URL = 'http://localhost:8000'

def get_jwt_token(username="admin", password="12345678"):
    """
    Helper function to get a JWT token for authorization.
    Returns:
        str: A valid JWT token.
    """
    auth_url = f"{BASE_URL}/login"

    data = {"username": username, "password": password}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    response = requests.post(auth_url, headers=headers, data=data)
    return response.json()["access_token"]