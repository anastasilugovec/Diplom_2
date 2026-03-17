from faker import Faker
import random
import time
from api.stellar_burgers_api import StellarBurgersAPI

faker = Faker()

def generate_name():
    return faker.first_name() + str(random.randint(100, 999))

def generate_email():
    return faker.email()

def generate_password(length=10):
    return faker.password(length=length)

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
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 403 and "User already exists" in response.text:
        return None
    else:
        raise Exception(f"Не удалось создать пользователя: {response.text}")

def get_static_user_data():
    return {
        "name": "StaticUser",
        "email": "staticuser@example.com",
        "password": "Password123!"
    }