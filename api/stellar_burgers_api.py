import requests
from urls import REGISTER_URL, LOGIN_URL, USER_URL, ORDER_URL, INGREDIENTS_URL, BASE_URL

class StellarBurgersAPI:

    @staticmethod
    def create_user(name, email, password):
        payload = {
            "name": name,
            "email": email,
            "password": password
        }
        return requests.post(REGISTER_URL, json=payload)

    @staticmethod
    def login(email, password):
        payload = {
            "email": email,
            "password": password
        }
        return requests.post(LOGIN_URL, json=payload)

    @staticmethod
    def get_user(access_token):
        headers = {
            "Authorization": access_token
        }
        return requests.get(USER_URL, headers=headers)

    @staticmethod
    def get_ingredients():
        return requests.get(INGREDIENTS_URL)

    @staticmethod
    def create_order(ingredients, access_token=None):
        headers = {
            "Content-Type": "application/json"
        }
        if access_token:
            headers["Authorization"] = access_token

        payload = {
            "ingredients": ingredients
        }
        return requests.post(ORDER_URL, json=payload, headers=headers)

    @staticmethod
    def delete_user(access_token):
        url = f"{BASE_URL}/auth/user"
        headers = {
            "Authorization": access_token
        }
        response = requests.delete(url, headers=headers)
        return response