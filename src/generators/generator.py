import random
import string


class TestDataGenerator:
    letters = string.ascii_lowercase

    @classmethod
    def generate_user_data(cls, length=8):
        email = cls.generate_email(length)
        password = cls.generate_password(length)
        username = cls.generate_username(length)
        return email, password, username

    @staticmethod
    def generate_email(length):
        username = ''.join(random.choice(TestDataGenerator.letters) for i in range(length))
        domain = ''.join(random.choice(TestDataGenerator.letters) for i in range(length))
        email = f"{username}@{domain}.com"
        return email

    @staticmethod
    def generate_password(length):
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    @staticmethod
    def generate_username(length):
        username = ''.join(random.choice(TestDataGenerator.letters) for i in range(length))
        return username


