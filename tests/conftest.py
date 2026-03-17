import pytest
from http import HTTPStatus
from api.stellar_burgers_api import StellarBurgersAPI
from helpers import generate_name, generate_password, generate_unique_email, generate_user_data, get_static_user_data, create_user_in_api
from data.test_data import StatusCodes

@pytest.fixture
def user_data():
    return get_static_user_data()

@pytest.fixture
def created_user(user_data):
    access_token = create_user_in_api(user_data)
    return {
        "accessToken": access_token,
        "user_data": user_data
    }

@pytest.fixture
def registered_user():
    user_data = generate_user_data()
    name = user_data['name']
    email = user_data['email']
    password = user_data['password']

    response = StellarBurgersAPI.create_user(name, email, password)

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
        try:
            StellarBurgersAPI.delete_user(token)
        except Exception as e:
            print(f"Ошибка при удалении пользователя: {e}")