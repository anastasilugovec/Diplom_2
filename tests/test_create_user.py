import pytest
import allure
from api.stellar_burgers_api import StellarBurgersAPI
from data.test_data import StatusCodes, ErrorMessages, ResponseFields

class TestCreateUser:

    @allure.title("Создание уже существующего пользователя")
    @allure.description("Тест проверяет обработку попытки создания дубликата пользователя")
    def test_create_existing_user(self, create_user_and_cleanup):
        # В этом тесте пользователь уже создан фикстурой
        user = create_user_and_cleanup

        # Попытка создать дубликат
        response = StellarBurgersAPI.create_user(user["name"], user["email"], user["password"])

        # Проверка, что ответ 403 и сообщение о существующем пользователе
        assert response.status_code == StatusCodes.FORBIDDEN
        assert response.json()[ResponseFields.MESSAGE] == ErrorMessages.USER_ALREADY_EXISTS