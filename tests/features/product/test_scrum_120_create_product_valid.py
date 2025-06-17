import requests
import time
from datetime import datetime

# Helpers
from helpers.auth_helper import get_jwt_token, BASE_URL

'''
  SCRUM-120 - Testcase: [POST] Create Product - Valid Input
  Objective: Verify the API response status, schema, SLA, and database entry when creating a product with valid input.
  Steps:
    1. Send API request with valid data.
  Expected Result:
    - Status code is 201.
    - Response schema should match the defined spec.
    - SLA should <= 3s.
    - Product is successfully created in the database.
'''

def test_scrum_120_create_product_valid(db_session):
    # Precondition: Retrieve a valid JWT token
    jwt_token = get_jwt_token()

    # Endpoint and headers
    url = f"{BASE_URL}/product/"
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Request payload
    payload = {
        "name": "Smartphone",
        "type": "Electronics",
        "retail_price": 699.99,
        "created_date": "2023-10-01T00:00:00Z"
    }

    # Step 1: Send API request with valid data
    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    response_time = time.time() - start_time

    # Validate status code is 201
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"

    # Validate response schema
    response_json = response.json()
    assert "id" in response_json, "Response missing 'id'"
    assert response_json["name"] == payload["name"], f"Expected name '{payload['name']}', got '{response_json['name']}'"
    assert response_json["type"] == payload["type"], f"Expected type '{payload['type']}', got '{response_json['type']}'"
    assert response_json["retail_price"] == payload["retail_price"], f"Expected retail_price '{payload['retail_price']}', got '{response_json['retail_price']}'"
    assert response_json["created_date"] == payload["created_date"], f"Expected created_date '{payload['created_date']}', got '{response_json['created_date']}'"

    # Validate SLA <= 3s
    assert response_time <= 3, f"Expected response time <= 3s, got {response_time}s"

    # Validate product is created in the database
    # Query the product by ID using the database session fixture
    from models.db_models import Product
    product_in_db = db_session.query(Product).filter(Product.id == response_json["id"]).first()
    assert product_in_db is not None, "Product not found in the database"
    assert product_in_db.name == payload["name"]
    assert product_in_db.type == payload["type"]
    assert product_in_db.retail_price == payload["retail_price"]
    # Compare datetime string to datetime object
    assert product_in_db.created_date == datetime.fromisoformat(payload["created_date"].replace("Z", "+00:00"))
