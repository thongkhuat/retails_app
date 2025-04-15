# tests/helpers/auth_helper.py
import requests

def get_jwt_token():
    """
    Helper function to get a JWT token for authorization.
    Returns:
        str: A valid JWT token.
    """
    auth_url = "http://localhost:8000/login"
    auth_payload = {
        "username": "admin",
        "password": "12345678"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(auth_url, headers=headers, json=auth_payload, verify=False)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json().get("token")