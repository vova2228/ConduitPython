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
@allure.title("Checking article offset")
@pytest.mark.order(4)
def test_check_articles_offset():
    with step("Get articles with default offset"):
        articles_first_page, response = articles_api.get_articles()
        offset = random.randint(1, 10)

    with step(f"Get articles with offset = {offset}"):
        articles_with_offset, response = articles_api.get_articles(offset=offset)

    with step("Check that the response body has valid data"):
        tests.check_articles_response(
            response, SuccessfullGetArticle.expected_keys, SuccessfullGetArticle.status_code)

    with step("Check default and offset article counts"):
        tests.check_response_article_count(10, len(articles_first_page.articles))
        tests.check_response_article_count(10, len(articles_with_offset.articles))

    with step("Check articles are different"):
        tests.check_articles_are_not_equal(articles_first_page, articles_with_offset)
