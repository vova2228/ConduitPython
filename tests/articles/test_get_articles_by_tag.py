import random
import allure
import pytest
from src.API.authorization_api.auth_api import AuthAPI
from src.utils.utils import Utils
from src.API.articles_api.articles_api import ArticlesApi
from tests.articles.articles_check import ArticlesTests

step = allure.step
utils = Utils()
articles_api = ArticlesApi()
auth_api = AuthAPI()
tests = ArticlesTests()


@allure.suite("Articles tests")
@allure.title("Get article by tag")
@pytest.mark.order(7)
def test_get_articles_by_tag():
    with step("Get all articles and filter by random tag"):
        limit = random.randint(10, 200)
        articles, response = articles_api.get_articles(limit=limit)
        random_article = (random.choice(articles.articles))
        tag_list = utils.get_tag_list_from_article(random_article)
        tag = random.choice(tag_list)
        expected_articles = [a for a in articles.articles if tag in a.tagList]

    with step(f"Get articles by tag with limit = {limit}"):
        articles_by_tag, response = articles_api.get_articles_by_tag(tag, limit=limit)

    with step("Compare articles with articles received by tag"):
        tests.check_articles_are_equal(expected_articles, articles_by_tag.articles)
