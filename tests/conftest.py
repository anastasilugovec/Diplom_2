import pytest
import allure
import logging
from api.stellar_burgers_api import StellarBurgersAPI
from helpers import generate_name, generate_password, generate_unique_email
from http import HTTPStatus

logger = logging.getLogger(__name__)

@pytest.fixture
def user():
    with allure.step("Генерация уникальных данных пользователя"):
        name = generate_name()
        email = generate_unique_email()
        password = generate_password()

    with allure.step("Создание пользователя через API"):
        response = StellarBurgersAPI.create_user(name, email, password)
        if response.status_code != HTTPStatus.OK:
            error_message = f"Не удалось создать пользователя. Status code: {response.status_code}, Response: {response.text}"
            logger.error(error_message)
            pytest.fail(error_message)

    with allure.step("Извлечение и форматирование access token"):
        response_data = response.json()
        access_token = response_data.get("accessToken")
        if not access_token:
            error_message = "Access token не получен при создании пользователя"
            logger.error(error_message)
            pytest.fail(error_message)

        if not access_token.startswith("Bearer "):
            access_token = f"Bearer {access_token}"

    return {
        "accessToken": access_token,
        "user_data": {
            "name": name,
            "email": email,
            "password": password
        }
    }

@pytest.fixture
def user_data():
    with allure.step("Генерация уникальных данных пользователя"):
        name = generate_name()
        email = generate_unique_email()
        password = generate_password()

    return {
        "name": name,
        "email": email,
        "password": password
    }

@pytest.fixture
def create_and_delete_user():
    name = generate_name()
    email = generate_unique_email()
    password = generate_password()

    response = StellarBurgersAPI.create_user(name, email, password)
    assert response.status_code == HTTPStatus.OK, "Не удалось создать пользователя перед тестом"
    response_data = response.json()
    access_token = response_data.get("accessToken")
    if not access_token:
        pytest.fail("Access token не получен при создании пользователя")
    if not access_token.startswith("Bearer "):
        access_token = f"Bearer {access_token}"

    yield {
        "name": name,
        "email": email,
        "password": password,
        "access_token": access_token
    }

    delete_response = StellarBurgersAPI.delete_user(access_token)
    if delete_response.status_code != HTTPStatus.OK:
        print(f"Не удалось удалить пользователя. Статус: {delete_response.status_code}")

# Объявляем create_test_user отдельно
@pytest.fixture
def create_test_user():
    def _create_user():
        name = generate_name()
        email = generate_unique_email()
        password = generate_password()

        response = StellarBurgersAPI.create_user(name, email, password)
        assert response is not None, "Ответ create_user равен None"
        assert response.status_code == HTTPStatus.OK, f"Ошибка при создании пользователя: {response.text}"

        return {
            "name": name,
            "email": email,
            "password": password
        }
    return _create_user

@pytest.fixture
def registered_user():
    name = generate_name()
    email = generate_unique_email()
    password = generate_password()
    response = StellarBurgersAPI.create_user(name, email, password)
    assert response.status_code == 200
    return {"name": name, "email": email, "password": password}