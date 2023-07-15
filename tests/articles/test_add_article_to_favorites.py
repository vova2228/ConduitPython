import random
import allure
import pytest
from src.API.authorization_api.request_type import RequestType
from src.expected_results.articles_expected_results import SuccessfullAddToFavorites
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


@allure.suite("Articles tests")
@allure.title("Add article to favorites")
@pytest.mark.order(9)
def test_add_article_to_favorites():
    random_offset = random.randint(1, 19)
    token = login_user.token

    with step("Get all articles"):
        articles, response = articles_api.get_articles(token=token, limit=10, offset=random_offset)

        slugs = []
        for article in articles.articles:
            slugs.append(article.slug)

        random_slug = random.choice(slugs)

    with step(f"Add article with slug ''{random_slug}'' to favorites"):
        articles, response = articles_api.add_article_to_favorites(slug=random_slug, token=token)
        tests.check_articles_response(
            response, SuccessfullAddToFavorites.expected_keys, SuccessfullAddToFavorites.status_code)
        tests.check_favorited(articles.articles, True)

    with step("Check article was added to favorites"):
        tests.check_article_was_added_to_favorites(slug=random_slug, token=token)

    with step("Delete article from favorites"):
        articles_api.delete_article_from_favorites(slug=random_slug, token=token)

    with step("Check article was deleted from favorites"):
        tests.check_article_was_deleted_from_favorites(slug=random_slug, token=token)
