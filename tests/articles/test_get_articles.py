import allure
import pytest
from tests.articles.articles_check import ArticlesTests
from src.expected_results.articles_expected_results import *
from src.API.articles_api.articles_api import ArticlesApi
from src.utils.utils import Utils

step = allure.step
utils = Utils


@allure.suite("Articles tests")
@allure.title("Getting articles without a token")
@pytest.mark.order(2)
def test_get_articles():
    with step("Get the article"):
        articles, response = ArticlesApi().get_articles(limit=1)

    with step("Check that the response body has valid data"):
        ArticlesTests().check_articles_response(
            response, SuccessfullGetArticle.expected_keys, SuccessfullGetArticle.status_code)
