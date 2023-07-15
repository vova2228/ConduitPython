import random
import string

letters = string.ascii_lowercase
digits = string.digits
bios = [
    "I love to code in Python!",
    "Software engineer and coffee addict",
    "Traveller and bookworm",
    "Foodie. Yoga enthusiast. Dog mom.",
    "Lifelong learner and problem solver"
]

comments = [
    "Nice",
    "Great",
    "Awesome",
    "Terrific",
    "Excellent",
    "Superb",
    "Brilliant",
    "Wonderful",
    "Amazing",
    "Interesting"
]


class TestDataGenerator:
    """
    Generates random test data.

    Methods:
        generate_user_data(length): Generates email, password and username.
        generate_email(length): Generates random email.
        generate_password(length): Generates random password.
        generate_username(length): Generates random username.
    """

    @staticmethod
    def get_random_comment():
        return random.choice(comments)

    def generate_user_data(self, length=8):
        email = self.generate_email(length)
        password = self.generate_password(length)
        username = self.generate_username(length)
        bio = self.generate_bio()
        return email, password, username, bio

    @classmethod
    def generate_email(cls, length=8):
        username = ''.join(random.choices(letters, k=length))
        domain = ''.join(random.choices(letters, k=length))
        email = f"{username}@{domain}.com"
        return email

    @classmethod
    def generate_password(cls, length=8):
        password = ''.join(random.choices(digits + letters, k=length))
        return password

    @classmethod
    def generate_username(cls, length=8):
        username = ''.join(random.choices(letters, k=length))
        return username

    @classmethod
    def generate_bio(cls, length=20):

        bio = random.choice(bios)
        if len(bio) < length:
            extra = "".join(random.choices(string.ascii_lowercase, k=length - len(bio)))
            bio += " " + extra
        elif len(bio) > length:
            bio = bio[:length]

        return bio
