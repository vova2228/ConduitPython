import random
import pytz
from datetime import datetime
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

    @staticmethod
    def get_now_date():
        date = datetime.utcnow().replace(tzinfo=pytz.utc)
        date = date.replace(second=0, microsecond=0).isoformat() + 'Z'
        return date

    @staticmethod
    def convert_article_date(date):
        date = datetime.fromisoformat(date).astimezone(pytz.utc).replace(second=0, microsecond=0).isoformat() + 'Z'
        return date
