import allure
import pytest
from flaky import flaky
from src.API.articles_api.articles_api import ArticlesApi
from src.API.authorization_api.auth_api import AuthAPI
from tests.articles.articles_check import ArticlesTests
from src.models.user import UserRequest, UserBody
from src.expected_results.articles_expected_results import *
from src.API.authorization_api.request_type import RequestType
from src.utils.utils import Utils

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
@allure.title("Post comment for article")
@pytest.mark.order(1)
@flaky(max_runs=3, min_passes=1)
def test_post_comment_for_article():
    token = login_user.token

    with step("Create article"):
        articles, _ = ArticlesApi().post_articles(token=token)
        slug = articles.articles.slug

    with step("Post article comment"):
        comments, response = ArticlesApi().post_article_comment(slug=slug, token=token)
        created_comment = comments.comments.body
        comment_id = comments.comments.id

        ArticlesTests().check_articles_response(response, SuccessfullPostComments.expected_keys,
                                                SuccessfullPostComments.status_code)

        date_created = Utils.convert_article_date(comments.comments.createdAt)
        now_date = Utils.get_now_date()

    with step("Get article comment"):
        comments, response = ArticlesApi().get_article_comments(slug=slug, token=token)
        get_comment = comments.comments[0].body
        ArticlesTests().check_articles_response(response, SuccessfullGetComments.expected_keys,
                                                SuccessfullGetComments.status_code)

    with step("Check comments and dates in responses"):
        ArticlesTests().check_dates_are_equal(date_created, now_date)
        ArticlesTests().check_comments_are_equal(created_comment, get_comment)
        ArticlesTests().check_articles_response(response, SuccessfullGetComments.expected_keys,
                                                SuccessfullGetComments.status_code)

    with step("Delete article comment"):
        response = ArticlesApi().delete_article_comment(slug=slug, token=token, comment_id=comment_id)
        ArticlesTests().check_articles_response(response, SuccessfullDeleteComments.expected_text,
                                                SuccessfullDeleteComments.status_code)

    with step("Check comment was deleted"):
        ArticlesTests().check_comment_was_deleted(slug, token)
