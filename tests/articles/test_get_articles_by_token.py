import allure
import pytest
from src.models.user import UserRequest
from src.API.authorization_api.auth_api import AuthAPI
from tests.articles.articles_check import ArticlesTests
from src.expected_results.articles_expected_results import *
from src.API.authorization_api.request_type import RequestType
from src.API.articles_api.articles_api import ArticlesApi
from src.utils.utils import Utils

step = allure.step
user: UserRequest


def setup_function():
    global user
    with step("Get the user from the file"):
        user = Utils.get_user(RequestType.login, is_random=False)


@allure.suite("Articles tests")
@allure.title("Getting articles by token")
@pytest.mark.order(1)
def test_get_articles_by_token():
    with step("Log in and get the token"):
        login_user, response = AuthAPI().login_user(user)
        token = login_user.token

    with step("Get the article by token"):
        articles, response = ArticlesApi().get_articles(token, limit=1)

    with step("Check that the response body has valid data"):
        ArticlesTests().check_articles_response(
            response, SuccessfullGetArticle.expected_keys, SuccessfullGetArticle.status_code)