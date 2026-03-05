import allure
from api.stellar_burgers_api import StellarBurgersAPI
from helpers import get_ingredients

class TestCreateOrder:

    def _get_ingredients(self):
        return get_ingredients()

    @allure.title("Создание заказа с авторизацией")
    @allure.description("Тест проверяет создание заказа авторизованным пользователем")
    def test_create_order_with_auth(self, user):
        with allure.step("Получение access token из фикстуры"):
            access_token = user["accessToken"]

        with allure.step("Получение списка ингредиентов"):
            ingredients = self._get_ingredients()[:2]

        with allure.step("Создание заказа с авторизацией"):
            response = StellarBurgersAPI.create_order(ingredients, access_token)

        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "order" in response.json()

    @allure.title("Создание заказа без авторизации")
    @allure.description("Тест проверяет создание заказа без токена авторизации")
    def test_create_order_without_auth(self):
        with allure.step("Получение списка ингредиентов"):
            ingredients = self._get_ingredients()[:2]

        with allure.step("Создание заказа без авторизации"):
            response = StellarBurgersAPI.create_order(ingredients)

        with allure.step("Проверка создания заказа без авторизации"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "order" in response.json()

    @allure.title("Создание заказа с ингредиентами")
    @allure.description("Тест проверяет создание заказа с валидными ингредиентами")
    def test_create_order_with_ingredients(self, user):
        with allure.step("Получение access token из фикстуры"):
            access_token = user["accessToken"]

        with allure.step("Получение списка ингредиентов"):
            ingredients = self._get_ingredients()[:2]

        with allure.step("Создание заказа с ингредиентами"):
            response = StellarBurgersAPI.create_order(ingredients, access_token)

        with allure.step("Проверка заказа с ингредиентами"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert len(response.json()["order"]["ingredients"]) > 0

    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Тест проверяет обработку пустого списка ингредиентов")
    def test_create_order_without_ingredients(self, user):
        with allure.step("Получение access token из фикстуры"):
            access_token = user["accessToken"]

        with allure.step("Создание заказа с пустым списком ингредиентов"):
            response = StellarBurgersAPI.create_order([], access_token)

        with allure.step("Проверка ошибки отсутствия ингредиентов"):
            assert response.status_code == 400
            assert response.json()["success"] is False

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.description("Тест проверяет обработку невалидных хешей ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, user):
        with allure.step("Получение access token из фикстуры"):
            access_token = user["accessToken"]

        with allure.step("Создание заказа с неверными хешами ингредиентов"):
            response = StellarBurgersAPI.create_order(["invalidHash123", "anotherInvalid456"], access_token)

        with allure.step("Проверка ошибки сервера"):
            assert response.status_code == 500