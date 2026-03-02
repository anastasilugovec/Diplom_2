import allure
import pytest
import logging
from api.stellar_burgers_api import StellarBurgersAPI
from helpers import generate_name, generate_password, generate_unique_email

logger = logging.getLogger(__name__)


@pytest.fixture
def user():

    with allure.step("Генерация уникальных данных пользователя"):
        name = generate_name()
        email = generate_unique_email()  # Используем гарантированно уникальный email
        password = generate_password()

    with allure.step("Создание пользователя через API"):
        response = StellarBurgersAPI.create_user(name, email, password)
        if response.status_code != 200:
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
def created_user(user):

    return user