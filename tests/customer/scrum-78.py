import pytest
import requests

@pytest.mark.parametrize("payload, expected_status, expected_response", [
    (
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email-format"
        },
        400,
        {
            "errorCode": "400",
            "errorMsg": "Invalid email format"
        }
    )
])
def test_invalid_email_format(api_base_url, auth_token, payload, expected_status, expected_response):
    url = f"{api_base_url}/customer/"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Assert status code
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

    # Assert response schema
    response_json = response.json()
    assert response_json == expected_response, f"Expected {expected_response}, got {response_json}"

    # Assert SLA
    assert response.elapsed.total_seconds() <= 3, f"SLA exceeded: {response.elapsed.total_seconds()}s"