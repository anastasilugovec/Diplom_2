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