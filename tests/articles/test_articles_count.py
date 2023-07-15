import allure
import pytest
import random
from src.API.authorization_api.auth_api import AuthAPI
from tests.articles.articles_check import ArticlesTests
from src.expected_results.articles_expected_results import *
from src.API.articles_api.articles_api import ArticlesApi
from src.utils.utils import Utils

step = allure.step
utils = Utils()
articles_api = ArticlesApi()
auth_api = AuthAPI()
tests = ArticlesTests()


@allure.suite("Articles tests")
@allure.title("Check the number of articles in the response")
@pytest.mark.order(3)
def test_articles_count():
    limit = random.randint(1, 100)
    with step(f"Get articles with limit = {limit}"):
        articles, response = articles_api.get_articles(limit=limit)

    with step("Check that the response body has valid data"):
        tests.check_articles_response(
            response, SuccessfullGetArticle.expected_keys, SuccessfullGetArticle.status_code)

    with step(f"Check that the number of articles in the response corresponds to limit = {limit}"):
        actual_count = len(articles.articles)
        tests.check_response_article_count(limit, actual_count)
