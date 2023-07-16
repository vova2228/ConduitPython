import allure
import pytest
from flaky import flaky
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
@allure.title("Checking article creation")
@pytest.mark.order(5)
@flaky(max_runs=3, min_passes=1)
def test_create_article():
    with step("Create an article by token"):
        token = login_user.token
        articles, response = ArticlesApi().post_articles(token=token)
        creation_date = Utils.convert_article_date(articles.articles.createdAt)
        date_now = Utils.get_now_date()

    with step("Check that the response body has valid data and date article created at"):
        ArticlesTests().check_articles_response(
            response, SuccessfullPostArticle.expected_keys, SuccessfullPostArticle.status_code)
        ArticlesTests().check_dates_are_equal(date_now, creation_date)
