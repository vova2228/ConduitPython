import allure
import pytest
from flaky import flaky
from src.API.authorization_api.request_type import RequestType
from src.expected_results.articles_expected_results import SuccessfullPostArticle, SuccessfullGetArticle
from src.API.authorization_api.auth_api import AuthAPI
from src.utils.utils import Utils
from src.models.user import UserRequest, UserBody
from src.API.articles_api.articles_api import ArticlesApi
from tests.articles.articles_check import ArticlesTests

step = allure.step
utils = Utils()
articles_api = ArticlesApi()
auth_api = AuthAPI()
tests = ArticlesTests()
user: UserRequest
login_user: UserBody


def setup_function():
    global user
    with step("Get the user from the file"):
        user = utils.get_user(RequestType.login, is_random=False)

    global login_user
    with step("Log in and get the token"):
        login_user, response = auth_api.login_user(user)


def teardown_function():
    utils.clear_user_articles(login_user)


@allure.suite("Articles tests")
@allure.title("Update article")
@pytest.mark.order(8)
@flaky(max_runs=3, min_passes=1)
def test_update_article():
    with step("Create an article by token"):
        token = login_user.token
        article_before_update, response = articles_api.post_articles(token=token)
        slug = article_before_update.articles.slug
        tests.check_articles_response(
            response, SuccessfullPostArticle.expected_keys, SuccessfullGetArticle.status_code)

    with step(f"Update article with slug ''{slug}''"):
        updated_article, response = articles_api.update_articles(slug=slug, token=token)
        slug = updated_article.articles.slug
        now_date = utils.get_now_date()
        tests.check_articles_response(
            response, SuccessfullPostArticle.expected_keys, SuccessfullPostArticle.status_code)

    with step(f"Get article with slug ''{slug}''"):
        new_article, response = articles_api.get_articles_by_slug(slug=slug, token=token)
        date_updated_at = utils.convert_article_date(new_article.articles.updatedAt)
        tests.check_articles_response(
            response, SuccessfullPostArticle.expected_keys, SuccessfullPostArticle.status_code)

    with step("Check articles are not equal and dates updated at"):
        tests.check_articles_are_not_equal(article_before_update, new_article)
        tests.check_dates_are_equal(now_date, date_updated_at)
