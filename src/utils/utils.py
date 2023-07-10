import random

from API.authorization_api.request_type import RequestType
from models.user import UserRequest


class Utils:

    @staticmethod
    def get_random_article(articles):
        if not articles:
            return None
        return articles[random.randint(0, len(articles) - 1)]

    @staticmethod
    def get_user(request_type: RequestType, is_random: bool = None):
        return UserRequest(request_type, is_random)
