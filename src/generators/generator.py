import random
import string


class TestDataGenerator:
    letters = string.ascii_lowercase

    def generate_user_data(self, length=8):
        email = self.generate_email(length)
        password = self.generate_password(length)
        username = self.generate_username(length)
        return email, password, username

    @classmethod
    def generate_email(cls, length=8):
        username = ''.join(random.choice(cls.letters) for i in range(length))
        domain = ''.join(random.choice(cls.letters) for i in range(length))
        email = f"{username}@{domain}.com"
        return email

    @classmethod
    def generate_password(cls, length=8):
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    @classmethod
    def generate_username(cls, length=8):
        username = ''.join(random.choice(TestDataGenerator.letters) for i in range(length))
        return username


