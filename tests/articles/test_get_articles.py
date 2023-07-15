import allure
import pytest
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
@allure.title("Getting articles without a token")
@pytest.mark.order(2)
def test_get_articles():
    with step("Get the article"):
        articles, response = articles_api.get_articles(limit=1)

    with step("Check that the response body has valid data"):
        tests.check_articles_response(
            response, SuccessfullGetArticle.expected_keys, SuccessfullGetArticle.status_code)
