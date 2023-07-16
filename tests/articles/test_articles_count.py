import allure
import pytest
import random
from tests.articles.articles_check import ArticlesTests
from src.expected_results.articles_expected_results import *
from src.API.articles_api.articles_api import ArticlesApi

step = allure.step


@allure.suite("Articles tests")
@allure.title("Check the number of articles in the response")
@pytest.mark.order(3)
def test_articles_count():
    limit = random.randint(1, 100)
    with step(f"Get articles with limit = {limit}"):
        articles, response = ArticlesApi().get_articles(limit=limit)

    with step("Check that the response body has valid data"):
        ArticlesTests().check_articles_response(
            response, SuccessfullGetArticle.expected_keys, SuccessfullGetArticle.status_code)

    with step(f"Check that the number of articles in the response corresponds to limit = {limit}"):
        actual_count = len(articles.articles)
        ArticlesTests().check_response_article_count(limit, actual_count)
