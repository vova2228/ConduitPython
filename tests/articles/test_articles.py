import random

import allure
import pytest

from API.authorization_api.auth_api import AuthAPI
from articles.articlesTests import ArticlesTests
from expected_results.articles_expected_results import SuccesfullGetArticle
from src.API.authorization_api.request_type import RequestType
from src.API.articles_api.articles_api import ArticlesApi
from utils.utils import Utils

step = allure.step
utils = Utils()


@allure.suite("Тесты статей")
class TestArticles:
    articles_api = ArticlesApi()
    auth_api = AuthAPI()
    tests = ArticlesTests()

    @allure.title("Получение статей по токену")
    @pytest.mark.order(1)
    def test_get_articles_by_token(self):
        with step("Получаем пользователя из файла"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Авторизуемся и получаем токен"):
            login_user, response = self.auth_api.login_user(user)
            token = login_user.token

        with step("Получаем статью по токену"):
            articles, response = self.articles_api.get_articles(token, limit=1)

        with step("Проверяем, что тело ответа в формате JSON"):
            self.tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            self.tests.check_articles_response(
                response, SuccesfullGetArticle.expected_keys, SuccesfullGetArticle.status_code)

    @allure.title("Получение статей без токена")
    @pytest.mark.order(2)
    def test_get_articles(self):
        with step("Получаем статью"):
            articles, response = self.articles_api.get_articles(limit=1)

        with step("Проверяем, что тело ответа в формате JSON"):
            self.tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            self.tests.check_articles_response(
                response, SuccesfullGetArticle.expected_keys, SuccesfullGetArticle.status_code)

    @allure.title("Проверка количества статей в ответе")
    @pytest.mark.order(3)
    def test_articles_count(self):
        with step("Получаем статьи"):
            limit = random.randint(1, 100)
            articles, response = self.articles_api.get_articles(limit=limit)

        with step("Проверяем, что тело ответа в формате JSON"):
            self.tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            self.tests.check_articles_response(
                response, SuccesfullGetArticle.expected_keys, SuccesfullGetArticle.status_code)

        with step(f"Проверяем, что количество статей в ответе соответствует limit = {limit}"):
            actual_count = len(articles.articles)
            self.tests.check_reponse_article_count(limit, actual_count)
