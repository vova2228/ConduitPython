import random
import allure
import pytest

from flaky import flaky
from src.API.authorization_api.auth_api import AuthAPI
from tests.articles.articles_check import ArticlesTests
from src.expected_results.articles_expected_results import *
from src.API.authorization_api.request_type import RequestType
from src.API.articles_api.articles_api import ArticlesApi
from src.utils.utils import Utils

step = allure.step
utils = Utils()
articles_api = ArticlesApi()
auth_api = AuthAPI()
tests = ArticlesTests()


@flaky(max_runs=2, min_passes=1)
@allure.suite("Articles tests")
class TestArticles:

    @allure.title("Getting articles by token")
    @pytest.mark.order(1)
    def test_get_articles_by_token(self):
        with step("Get the user from the file"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Log in and get the token"):
            login_user, response = auth_api.login_user(user)
            token = login_user.token

        with step("Get the article by token"):
            articles, response = articles_api.get_articles(token, limit=1)

        with step("Check that the response body has valid data"):
            tests.check_articles_response(
                response, SuccessfullGetArticle.expected_keys, SuccessfullGetArticle.status_code)

    @allure.title("Getting articles without a token")
    @pytest.mark.order(2)
    def test_get_articles(self):
        with step("Get the article"):
            articles, response = articles_api.get_articles(limit=1)

        with step("Check that the response body has valid data"):
            tests.check_articles_response(
                response, SuccessfullGetArticle.expected_keys, SuccessfullGetArticle.status_code)

    @allure.title("Checking the number of articles in the response")
    @pytest.mark.order(3)
    def test_articles_count(self):
        limit = random.randint(1, 100)
        with step(f"Get articles with limit = {limit}"):
            articles, response = articles_api.get_articles(limit=limit)

        with step("Check that the response body has valid data"):
            tests.check_articles_response(
                response, SuccessfullGetArticle.expected_keys, SuccessfullGetArticle.status_code)

        with step(f"Check that the number of articles in the response corresponds to limit = {limit}"):
            actual_count = len(articles.articles)
            tests.check_response_article_count(limit, actual_count)

    @allure.title("Checking article offset")
    @pytest.mark.order(4)
    def test_check_articles_offset(self):
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

    @allure.title("Checking article creation")
    @pytest.mark.order(5)
    def test_create_article(self):
        with step("Get the user from the file"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Log in and get the token"):
            login_user, response = auth_api.login_user(user)
            token = login_user.token
            author = login_user.username

        with step("Create an article by token"):
            articles, response = articles_api.post_articles(token=token)
            slug = articles.articles.slug
            creation_date = utils.convert_article_date(articles.articles.createdAt)
            date_now = utils.get_now_date()

        with step("Check that the response body has valid data and date article created at"):
            tests.check_articles_response(
                response, SuccessfullPostArticle.expected_keys, SuccessfullPostArticle.status_code)
            tests.check_dates_are_equal(date_now, creation_date)

        with step("Delete the article"):
            response = articles_api.delete_article(token=token, slug=slug)
            tests.check_articles_response(
                response, SuccessfullDeleteArticle.expected_text, SuccessfullDeleteArticle.status_code)

        with step("Check article was deleted"):
            tests.check_article_was_deleted(author, token)

    @allure.title("Get article by author name")
    @pytest.mark.order(6)
    def test_get_articles_by_author(self):
        with step("Get the user from the file"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Log in and get the token"):
            login_user, response = auth_api.login_user(user)
            token = login_user.token
            author = login_user.username

        with step("Create an article by token"):
            articles, response = articles_api.post_articles(token=token)
            slug = articles.articles.slug
            author_from_article = articles.articles.author.username

        with step('Get articles by author name'):
            articles_by_author, response = articles_api.get_articles_by_author(author, token)

        with step("Check that the response body has valid data"):
            tests.check_articles_response(
                response, SuccessfullPostArticle.expected_keys, SuccessfullPostArticle.status_code)

        with step("Compare the author from the response with the author when creating the article"):
            tests.check_authors_are_equal(author, author_from_article)

        with step("Delete the article"):
            response = articles_api.delete_article(token=token, slug=slug)
            tests.check_articles_response(
                response, SuccessfullDeleteArticle.expected_text, SuccessfullDeleteArticle.status_code)

        with step("Check article was deleted"):
            tests.check_article_was_deleted(author, token)

    @allure.title("Get article by tag")
    @pytest.mark.order(7)
    def test_get_articles_by_tag(self):
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

    @allure.title("Update article")
    @pytest.mark.order(8)
    def test_update_article(self):
        with step("Get the user from the file"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Log in and get the token"):
            login_user, _ = auth_api.login_user(user)
            token = login_user.token
            author = login_user.username

        with step("Create an article by token"):
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

        with step("Delete article"):
            response = articles_api.delete_article(slug=slug, token=token)
            tests.check_articles_response(
                response, SuccessfullDeleteArticle.expected_text, SuccessfullDeleteArticle.status_code)

        with step("Check article was deleted"):
            tests.check_article_was_deleted(author, token)

    @allure.title("Add article to favorites")
    @pytest.mark.order(9)
    def test_add_article_to_favorites(self):
        random_offset = random.randint(1, 19)
        with step("Get the user from the file"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Log in and get the token"):
            login_user, response = auth_api.login_user(user)
            token = login_user.token
            author = login_user.username

        with step("Get all articles"):
            articles, response = articles_api.get_articles(token=token, limit=10, offset=random_offset)

            slugs = []
            for article in articles.articles:
                slugs.append(article.slug)

            random_slug = random.choice(slugs)

        with step(f"Add article with slug ''{random_slug}'' to favorites"):
            articles, response = articles_api.add_article_to_favorite(slug=random_slug, token=token)
            tests.check_articles_response(response, SuccessfullAddToFavorites.expected_keys, SuccessfullAddToFavorites.status_code)

        with step("Check article was added to favorites"):
            articles, response = articles_api.get_articles_by_slug(slug=random_slug, token=token)
            tests.check_article_is_favorited(articles)