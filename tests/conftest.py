import pytest
import allure

from api.stellar_burgers_api import StellarBurgersAPI
from helpers import generate_name, generate_password, generate_unique_email, generate_user_data, create_user_in_api
from data.test_data import StatusCodes, ErrorMessages, ResponseFields



@pytest.fixture
def user_data():
    return {
        'name': 'TestUser',
        'email': 'test@example.com',
        'password': 'Password123!'
    }

@pytest.fixture
def created_user(user_data):

    access_token = create_user_in_api(user_data)
    return {
        "accessToken": access_token,
        "user_data": user_data
    }

@pytest.fixture
def registered_user():
    name = generate_name()
    email = generate_unique_email()
    password = generate_password()

    response = StellarBurgersAPI.create_user(name, email, password)
    assert response.status_code == StatusCodes.SUCCESS
    access_token = response.json().get("accessToken")
    user = {
        "name": name,
        "email": email,
        "password": password,
        "accessToken": access_token
    }

    yield user

    if access_token:
        token = access_token
        if not token.startswith("Bearer "):
            token = f"Bearer {token}"
        StellarBurgersAPI.delete_user(token)

@pytest.fixture
def user_data():
    return generate_user_data()