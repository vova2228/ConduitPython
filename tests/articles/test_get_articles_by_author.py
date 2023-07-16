import allure
import pytest
from src.models.user import UserRequest, UserBody
from src.API.articles_api.request_type import RequestType
from src.API.authorization_api.auth_api import AuthAPI
from src.expected_results.articles_expected_results import *
from src.utils.utils import Utils
from src.API.authorization_api.request_type import RequestType
from src.API.articles_api.articles_api import ArticlesApi
from tests.articles.articles_check import ArticlesTests

step = allure.step
user: UserRequest
login_user: UserBody


def setup_function():
    global user
    with step("Get the user from the file"):
        user = Utils.get_user(RequestType.login, is_random=False)

    global login_user
    with step("Log in and get the token"):
        login_user, response = AuthAPI().login_user(user)


def teardown_function():
    Utils.clear_user_articles(login_user)


@allure.suite("Articles tests")
@allure.title("Get article by author name")
@pytest.mark.order(6)
def test_get_articles_by_author():
    with step("Create an article by token"):
        token = login_user.token
        author = login_user.username
        articles, response = ArticlesApi().post_articles(token=token)
        author_from_article = articles.articles.author.username

    with step('Get articles by author name'):
        articles_by_author, response = ArticlesApi().get_articles_by_author(author, token)

    with step("Check that the response body has valid data"):
        ArticlesTests().check_articles_response(
            response, SuccessfullPostArticle.expected_keys, SuccessfullPostArticle.status_code)

    with step("Compare the author from the response with the author when creating the article"):
        ArticlesTests().check_authors_are_equal(author, author_from_article)
