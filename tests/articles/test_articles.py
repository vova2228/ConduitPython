import allure
import pytest

from API.authorization_api.auth_api import AuthAPI
from articles.articlesTests import ArticlesTests
from expected_results.articles_expected_results import SuccesfullGetArticle
from src.API.authorization_api.request_type import RequestType
from src.models.user import UserRequest
from src.API.articles_api.articles_api import ArticlesApi
from utils.utils import Utils

step = allure.step

@allure.suite("Тесты статей")
class TestAuth:
    articles_api = ArticlesApi()
    auth_api = AuthAPI()
    tests = ArticlesTests()

    @allure.title("Получение статей по токену")
    @pytest.mark.order(1)
    def test_get_articles_by_token(self):
        with step("Получаем пользователя из файла"):
            user = UserRequest(RequestType.login, is_random=False)

        with step("Авторизуемся и получаем токен"):
            login_user, response = self.auth_api.login_user(user)
            token = login_user.token

        with step("Получаем статью по токену"):
            articles, response = self.articles_api.get_article(token, limit=5)

        with step("Проверяем, что тело ответа в формате JSON"):
            self.tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            self.tests.check_auth_response(response, SuccesfullGetArticle.expected_keys, SuccesfullGetArticle.status_code)

            # ran_article = Utils.get_random_article(articles.articles)
            # print(ran_article)

