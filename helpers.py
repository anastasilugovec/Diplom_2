from faker import Faker
import random
import time
from api.stellar_burgers_api import StellarBurgersAPI

faker = Faker()

def generate_name():
    return faker.first_name() + str(random.randint(100, 999))

def generate_email():
    return faker.email()

def generate_password():
    return faker.password(length=10)

def generate_unique_email():
    timestamp = int(time.time() * 1000)
    random_suffix = random.randint(1000, 9999)
    return f"test_{timestamp}_{random_suffix}@example.com"

def get_ingredients():
    response = StellarBurgersAPI.get_ingredients()
    assert response.status_code == 200, "Ошибка при получении ингредиентов"
    return [ingredient["_id"] for ingredient in response.json()["data"]]

def generate_user_data():
    name = generate_name()
    email = generate_unique_email()
    password = generate_password()
    return {
        "name": name,
        "email": email,
        "password": password
    }

def create_user_in_api(user_data):
    response = StellarBurgersAPI.create_user(user_data["name"], user_data["email"], user_data["password"])
    if response.status_code != 200:
        raise Exception(f"Не удалось создать пользователя: {response.text}")
    response_data = response.json()
    access_token = response_data.get("accessToken")
    if not access_token:
        raise Exception("Access token не получен при создании пользователя")
    if not access_token.startswith("Bearer "):
        access_token = f"Bearer {access_token}"
    return access_token
