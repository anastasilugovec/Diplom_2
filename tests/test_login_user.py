import allure
import pytest
from api.stellar_burgers_api import StellarBurgersAPI
from helpers import generate_name, generate_password, generate_unique_email


class TestLoginUser:

    @allure.title("Успешная авторизация пользователя")
    @allure.description("Тест проверяет вход с корректными учетными данными")
    def test_login_with_correct_credentials(self):
        with allure.step("Генерация тестовых данных"):
            name = generate_name()
            email = generate_unique_email()  # Используем гарантированно уникальный email
            password = generate_password()

        with allure.step("Создание пользователя"):
            create_response = StellarBurgersAPI.create_user(name, email, password)
            assert create_response.status_code == 200

        with allure.step("Авторизация пользователя"):
            login_response = StellarBurgersAPI.login_user(email, password)

        with allure.step("Проверка успешной авторизации"):
            assert login_response.status_code == 200
            assert "accessToken" in login_response.json()
            assert login_response.json()["success"] is True

    @allure.title("Авторизация с неверными учетными данными")
    @allure.description("Тест проверяет обработку неверного логина и пароля")
    def test_login_with_wrong_credentials(self):
        with allure.step("Отправка запроса с неверными учетными данными"):
            response = StellarBurgersAPI.login_user("wrong@example.com", "wrongpass")

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            assert response.json()["message"] == "email or password are incorrect"
            assert response.json()["success"] is False