import random

from src.API.authorization_api.request_type import RequestType
from src.models.user import UserRequest


class Utils:

    @staticmethod
    def get_random_article(articles):
        if not articles:
            return None
        return articles[random.randint(0, len(articles) - 1)]

    @staticmethod
    def get_user(request_type: RequestType, is_random: bool = None):
        return UserRequest(request_type, is_random)

    @staticmethod
    def get_tag_list_from_article(article) -> list:
        tag_list = article.tagList
        return tag_list
