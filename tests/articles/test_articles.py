import random
import allure
import pytest

from src.API.authorization_api.auth_api import AuthAPI
from tests.articles.articlesTests import ArticlesTests
from src.expected_results.articles_expected_results import *
from src.API.authorization_api.request_type import RequestType
from src.API.articles_api.articles_api import ArticlesApi
from src.utils.utils import Utils

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
                response, Successfullgetarticle.expected_keys, Successfullgetarticle.status_code)

    @allure.title("Получение статей без токена")
    @pytest.mark.order(2)
    def test_get_articles(self):
        with step("Получаем статью"):
            articles, response = self.articles_api.get_articles(limit=1)

        with step("Проверяем, что тело ответа в формате JSON"):
            self.tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            self.tests.check_articles_response(
                response, Successfullgetarticle.expected_keys, Successfullgetarticle.status_code)

    @allure.title("Проверка количества статей в ответе")
    @pytest.mark.order(3)
    def test_articles_count(self):
        limit = random.randint(1, 100)
        with step(f"Получаем статьи c limit = {limit}"):
            articles, response = self.articles_api.get_articles(limit=limit)

        with step("Проверяем, что тело ответа в формате JSON"):
            self.tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            self.tests.check_articles_response(
                response, Successfullgetarticle.expected_keys, Successfullgetarticle.status_code)

        with step(f"Проверяем, что количество статей в ответе соответствует limit = {limit}"):
            actual_count = len(articles.articles)
            self.tests.check_response_article_count(limit, actual_count)


    def test_create_article(self):
        with step("Получаем пользователя из файла"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Авторизуемся и получаем токен"):
            login_user, response = self.auth_api.login_user(user)
            token = login_user.token

        with step("Создаем статью по токену"):
            articles, response = self.articles_api.post_articles(token)
            slug = articles.articles.slug

        with step("Проверяем, что тело ответа имеет корректные данные"):
            self.tests.check_articles_response(
                response, SuccessfullPostArticle.expected_keys, SuccessfullPostArticle.status_code)

        with step("Удаляем статью"):
           response = self.articles_api.delete_article(token=token, slug=slug)
           self.tests.check_articles_response(
               response, SuccessfullDeleteArticle.expected_text, SuccessfullDeleteArticle.status_code)