import random
import allure
import pytz
from datetime import datetime
from src.expected_results.articles_expected_results import SuccessfullDeleteArticle
from src.API.articles_api.articles_api import ArticlesApi
from tests.articles.articles_check import ArticlesTests
from src.API.authorization_api.request_type import RequestType
from src.models.user import UserRequest

step = allure.step
articles_api = ArticlesApi()
tests = ArticlesTests()


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

    @staticmethod
    def clear_user_articles(user):
        with step("Delete articles for user"):
            token = user.token
            author = user.username

            articles, _ = articles_api.get_articles_by_author(author, token)

            for article in articles.articles:
                slug = article.slug
                response = articles_api.delete_article(token=token, slug=slug)
                tests.check_articles_response(response, SuccessfullDeleteArticle.expected_text,
                                              SuccessfullDeleteArticle.status_code)

                tests.check_article_was_deleted(author, token)
