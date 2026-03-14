import allure
from api.stellar_burgers_api import StellarBurgersAPI



class TestLoginUser:
    @allure.title("Успешная авторизация пользователя")
    @allure.description("Тест проверяет вход с корректными учетными данными")
    def test_login_with_correct_credentials(self, registered_user):
        with allure.step("Авторизация пользователя"):
            login_response = StellarBurgersAPI.login(registered_user['email'], registered_user['password'])

        with allure.step("Проверка успешной авторизации"):
            assert login_response.status_code == 200
            json_response = login_response.json()
            assert "accessToken" in json_response
            assert json_response["success"] is True

    @allure.title("Авторизация с неверными учетными данными")
    @allure.description("Тест проверяет обработку неверного логина и пароля")
    def test_login_with_wrong_credentials(self):
        with allure.step("Отправка запроса с неверными учетными данными"):
            response = StellarBurgersAPI.login("wrong@example.com", "wrongpass")
        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            json_response = response.json()
            assert json_response["message"] == "email or password are incorrect"
            assert json_response["success"] is False