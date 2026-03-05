import allure
import pytest
from api.stellar_burgers_api import StellarBurgersAPI
from helpers import generate_name, generate_password, generate_unique_email
from data.test_data import StatusCodes, ErrorMessages, ResponseFields, TestData

class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    @allure.description("Тест проверяет успешное создание нового пользователя")
    def test_create_unique_user(self):
        with allure.step("Генерация тестовых данных"):
            name = generate_name()
            email = generate_unique_email()
            password = generate_password()

        with allure.step("Отправка запроса на создание пользователя"):
            response = StellarBurgersAPI.create_user(name, email, password)

        with allure.step("Проверка успешного создания пользователя"):
            assert response.status_code == StatusCodes.SUCCESS
            assert response.json()[ResponseFields.SUCCESS] is True
            assert ResponseFields.ACCESS_TOKEN in response.json()

    @allure.title("Создание уже существующего пользователя")
    @allure.description("Тест проверяет обработку попытки создания дубликата пользователя")
    def test_create_existing_user(self):
        # Генерируем тестовые данные
        name = generate_name()
        email = generate_unique_email()
        password = generate_password()

        # Первое создание
        first_response = StellarBurgersAPI.create_user(name, email, password)
        assert first_response.status_code == StatusCodes.SUCCESS

        # Попытка создать дубликат
        second_response = StellarBurgersAPI.create_user(name, email, password)

        with allure.step("Проверка ошибки дублирования пользователя"):
            assert second_response.status_code == StatusCodes.FORBIDDEN
            assert second_response.json()[ResponseFields.MESSAGE] == ErrorMessages.USER_ALREADY_EXISTS

        # Удаляем пользователя вручную
        access_token = first_response.json().get("accessToken")
        if access_token:
            if not access_token.startswith("Bearer "):
                access_token = f"Bearer {access_token}"
            StellarBurgersAPI.delete_user(access_token)

    @allure.title("Создание пользователя без пароля")
    @allure.description("Тест проверяет валидацию при создании пользователя без пароля")
    def test_create_user_missing_password(self):
        with allure.step("Генерация тестовых данных с пустым паролем"):
            name = generate_name()
            email = generate_unique_email()
            password = TestData.EMPTY_PASSWORD

        with allure.step("Отправка запроса с отсутствующим паролем"):
            response = StellarBurgersAPI.create_user(name, email, password)

        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == StatusCodes.FORBIDDEN
            assert response.json()[ResponseFields.MESSAGE] == ErrorMessages.REQUIRED_FIELDS_MISSING

    @allure.title("Создание пользователя без имени")
    @allure.description("Тест проверяет валидацию при создании пользователя без имени")
    def test_create_user_missing_name(self):
        with allure.step("Генерация тестовых данных с пустым именем"):
            name = TestData.EMPTY_NAME
            email = generate_unique_email()
            password = generate_password()

        with allure.step("Отправка запроса с отсутствующим именем"):
            response = StellarBurgersAPI.create_user(name, email, password)

        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == StatusCodes.FORBIDDEN
            assert response.json()[ResponseFields.MESSAGE] == ErrorMessages.REQUIRED_FIELDS_MISSING

    @allure.title("Создание пользователя без email")
    @allure.description("Тест проверяет валидацию при создании пользователя без email")
    def test_create_user_missing_email(self):
        with allure.step("Генерация тестовых данных с пустым email"):
            name = generate_name()
            email = TestData.EMPTY_EMAIL
            password = generate_password()

        with allure.step("Отправка запроса с отсутствующим email"):
            response = StellarBurgersAPI.create_user(name, email, password)

        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == StatusCodes.FORBIDDEN
            assert response.json()[ResponseFields.MESSAGE] == ErrorMessages.REQUIRED_FIELDS_MISSING