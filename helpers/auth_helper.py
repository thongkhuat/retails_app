import requests

def get_jwt_token(base_url, username, password):
    """Fetch JWT token from the /login endpoint."""
    url = f"{base_url}/login"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Failed to fetch JWT token: {response.status_code}, {response.text}")