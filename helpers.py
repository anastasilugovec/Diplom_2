from faker import Faker
import random
import time

faker = Faker()

def generate_name():
    return faker.first_name() + str(random.randint(100, 999))

def generate_email():
    return faker.email()

def generate_password():
    return faker.password(length=10)

def generate_unique_email():
    """Генерирует гарантированно уникальный email с временной меткой"""
    timestamp = int(time.time() * 1000)
    random_suffix = random.randint(1000, 9999)
    return f"test_{timestamp}_{random_suffix}@example.com"