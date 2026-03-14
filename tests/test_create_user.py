import pytest
import allure
from api.stellar_burgers_api import StellarBurgersAPI
from data.test_data import StatusCodes, ErrorMessages, ResponseFields
from helpers import generate_name, generate_unique_email, generate_password


class TestCreateUser:

    @allure.title("Создание уже существующего пользователя")
    @allure.description("Тест проверяет, что при попытке создать пользователя с уже существующими данными API возвращает ошибку 403")
    def test_create_user_duplicate(self):

        user = {
            'name': generate_name(),
            'email': generate_unique_email(),
            'password': generate_password()
        }

        response_create = StellarBurgersAPI.create_user(user['name'], user['email'], user['password'])
        assert response_create.status_code == StatusCodes.SUCCESS, "Ошибка при создании пользователя впервые"


        response_duplicate = StellarBurgersAPI.create_user(user['name'], user['email'], user['password'])
        assert response_duplicate.status_code == 403, f"Ожидался статус 403, получен {response_duplicate.status_code}"

        message = response_duplicate.json().get(ResponseFields.MESSAGE)
        assert message == ErrorMessages.USER_ALREADY_EXISTS, f"Ожидалось сообщение '{ErrorMessages.USER_ALREADY_EXISTS}', получено '{message}'"
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        name = generate_name()
        email = generate_unique_email()
        password = generate_password()

        response = StellarBurgersAPI.create_user(name, email, password)
        assert response.status_code == StatusCodes.SUCCESS
        response_json = response.json()
        assert "accessToken" in response_json

        token = response_json["accessToken"]
        if not token.startswith("Bearer "):
            token = f"Bearer {token}"
        StellarBurgersAPI.delete_user(token)

    @allure.title("Создание пользователя без имени")
    def test_create_user_without_name(self):
        email = generate_unique_email()
        password = generate_password()

        response = StellarBurgersAPI.create_user("", email, password)
        assert response.status_code == StatusCodes.BAD_REQUEST


    @allure.title("Создание пользователя без email")
    def test_create_user_without_email(self):
        name = generate_name()
        password = generate_password()

        response = StellarBurgersAPI.create_user(name, "", password)
        assert response.status_code == StatusCodes.BAD_REQUEST

    @allure.title("Создание пользователя без пароля")
    def test_create_user_without_password(self):
        name = generate_name()
        email = generate_unique_email()

        response = StellarBurgersAPI.create_user(name, email, "")
        assert response.status_code == StatusCodes.BAD_REQUEST