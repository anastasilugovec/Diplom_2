import pytest
import allure
from api.stellar_burgers_api import StellarBurgersAPI
from data.test_data import StatusCodes, ErrorMessages, ResponseFields
from helpers import generate_name, generate_unique_email, generate_password

class TestCreateUser:

    @allure.title("Создание уже существующего пользователя")
    def test_create_user_duplicate(self):
        user = {
            'name': generate_name(),
            'email': generate_unique_email(),
            'password': generate_password()
        }

        with allure.step("Создание пользователя впервые"):
            response_create = StellarBurgersAPI.create_user(user['name'], user['email'], user['password'])
            assert response_create.status_code == StatusCodes.SUCCESS, "Ошибка при создании пользователя впервые"

        with allure.step("П попытке создать пользователя с теми же данными"):
            response_duplicate = StellarBurgersAPI.create_user(user['name'], user['email'], user['password'])
            assert response_duplicate.status_code == 403, f"Ожидался статус 403, получен {response_duplicate.status_code}"

        with allure.step("Проверка сообщения об ошибке при дублировании пользователя"):
            message = response_duplicate.json().get(ResponseFields.MESSAGE)
            assert message == ErrorMessages.USER_ALREADY_EXISTS, f"Ожидалось сообщение '{ErrorMessages.USER_ALREADY_EXISTS}', получено '{message}'"

    @allure.title("Создание пользователя без имени, email или пароля")
    @pytest.mark.parametrize("name, email, password, expected_status", [
        ("", generate_unique_email(), generate_password(), StatusCodes.FORBIDDEN),
        (generate_name(), "", generate_password(), StatusCodes.FORBIDDEN),
        (generate_name(), generate_unique_email(), "", StatusCodes.FORBIDDEN),
    ])
    def test_create_user_invalid_data(self, name, email, password, expected_status):
        with allure.step("Попытка создать пользователя с некорректными данными"):
            response = StellarBurgersAPI.create_user(name, email, password)
            assert response.status_code == expected_status