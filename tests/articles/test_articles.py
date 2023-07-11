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
articles_api = ArticlesApi()
auth_api = AuthAPI()
tests = ArticlesTests()


@allure.suite("Тесты статей")
class TestArticles:

    @allure.title("Getting articles by token")
    @pytest.mark.order(1)
    def test_get_articles_by_token(self):
        with step("Get the user from the file"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Log in and get the token"):
            login_user, response = auth_api.login_user(user)
            token = login_user.token

        with step("Get the article by token"):
            articles, response = articles_api.get_articles(token, limit=1)

        with step("Check that the response body is in JSON format"):
            tests.check_response_is_json(response)

        with step("Check that the response body has valid data"):
            tests.check_articles_response(
                response, Successfullgetarticle.expected_keys, Successfullgetarticle.status_code)


    @allure.title("Getting articles without a token")
    @pytest.mark.order(2)
    def test_get_articles(self):
        with step("Get the article"):
            articles, response = articles_api.get_articles(limit=1)

        with step("Check that the response body is in JSON format"):
            tests.check_response_is_json(response)

        with step("Check that the response body has valid data"):
            tests.check_articles_response(
                response, Successfullgetarticle.expected_keys, Successfullgetarticle.status_code)


    @allure.title("Checking the number of articles in the response")
    @pytest.mark.order(3)
    def test_articles_count(self):
        limit = random.randint(1, 100)
        with step(f"Get articles with limit = {limit}"):
            articles, response = articles_api.get_articles(limit=limit)

        with step("Check that the response body is in JSON format"):
            tests.check_response_is_json(response)

        with step("Check that the response body has valid data"):
            tests.check_articles_response(
                response, Successfullgetarticle.expected_keys, Successfullgetarticle.status_code)

        with step(f"Check that the number of articles in the response corresponds to limit = {limit}"):
            actual_count = len(articles.articles)
            tests.check_response_article_count(limit, actual_count)


    @allure.title("Checking article creation")
    @pytest.mark.order(4)
    def test_create_article(self):
        with step("Get the user from the file"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Log in and get the token"):
            login_user, response = auth_api.login_user(user)
            token = login_user.token

        with step("Create an article by token"):
            articles, response = articles_api.post_articles(token)
            slug = articles.articles.slug

        with step("Check that the response body has valid data"):
            tests.check_articles_response(
                response, SuccessfullPostArticle.expected_keys, SuccessfullPostArticle.status_code)

        with step("Delete the article"):
            response = articles_api.delete_article(token=token, slug=slug)
            tests.check_articles_response(
                response, SuccessfullDeleteArticle.expected_text, SuccessfullDeleteArticle.status_code)
