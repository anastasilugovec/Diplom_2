import pytest
import allure

from api.stellar_burgers_api import StellarBurgersAPI
from helpers import generate_name, generate_password, generate_unique_email
from data.test_data import StatusCodes, ErrorMessages, ResponseFields


@pytest.fixture
def user_data():
    """
    Генерирует и возвращает словарь с данными пользователя: имя, email, пароль.
    """
    return generate_user_data()

@pytest.fixture
def created_user(user_data):
    """
    Создает пользователя через API и возвращает словарь с accessToken и данными пользователя.
    """
    access_token = create_user_in_api(user_data)
    return {
        "accessToken": access_token,
        "user_data": user_data
    }
@pytest.fixture
def create_user_and_cleanup():
    created_user = None
    try:
        # Генерация данных
        name = generate_name()
        email = generate_unique_email()
        password = generate_password()

        response = StellarBurgersAPI.create_user(name, email, password)
        assert response.status_code == StatusCodes.SUCCESS
        created_user = {
            "name": name,
            "email": email,
            "password": password,
            "accessToken": response.json().get("accessToken")
        }

        yield created_user

    finally:
        if created_user and created_user["accessToken"]:
            token = created_user["accessToken"]
            if not token.startswith("Bearer "):
                token = f"Bearer {token}"
            StellarBurgersAPI.delete_user(token)


@pytest.fixture
def registered_user():
    # Создаем пользователя через API
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

    # Удаляем пользователя после теста
    if access_token:
        token = access_token
        if not token.startswith("Bearer "):
            token = f"Bearer {token}"
        StellarBurgersAPI.delete_user(token)
