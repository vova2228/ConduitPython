from requests import Response
from src.API.articles_api.articles_api import ArticlesApi
from tests.basic_check import BaseCheck

articles_api = ArticlesApi()


class ArticlesTests(BaseCheck):

    @classmethod
    def check_articles_response(cls, response: Response, expected_text: list | str, expected_status_code):

        """
        Checks that an API response contains expected text and has an expected status code.

        Args:
            response (Response): The API response.
            expected_text (list | str): The expected text in the response body. Can be a list of keys or a string.
            expected_status_code (int): The expected HTTP status code of the response.
        """

        print("Checking the response body...")
        if isinstance(expected_text, list):
            for key in expected_text:
                assert key in response.text, f"The server response does not contain the key {key}!!"
        else:
            assert expected_text in response.text, f"The server response does not contain the text {expected_text}!!"

        cls.check_status_code(response, expected_status_code)
        cls.check_response_is_json(response)

    @classmethod
    def check_response_article_count(cls, expected_count, actual_count):

        """
        Checks that the number of articles in an API response matches an expected count.

        Args:
            expected_count (int): The expected number of articles in the response.
            actual_count (int): The actual number of articles in the response.
        """

        print(
            f"Check that the number of requested articles {expected_count} = the number of received articles {actual_count}")
        assert expected_count == actual_count, f"The number of articles in the response should be equal to {expected_count}, but the number = {actual_count}"

    @classmethod
    def check_article_was_deleted(cls, author, token):

        """
       Checks if an article for a given author has been deleted.

       Args:
           author (str): The username of the article's author.
           token (str): The authentication token.
       """

        articles, response = articles_api.get_articles_by_author(author, token)
        assert articles.articlesCount == 0, f"The article for ''{author}'' was not deleted!!"
        print(f"Article for ''{author}'' was deleted")
        cls.check_status_code(response, 200)
        cls.check_response_is_json(response)

    @staticmethod
    def check_articles_are_not_equal(first_articles, sec_articles):
        print("Checking articles are not equal...")
        assert first_articles != sec_articles, "First articles response is equal sec article response!!"

    @staticmethod
    def check_articles_are_equal(first_articles: list, sec_articles: list):
        print("Checking articles are equal...")
        for article in first_articles:
            assert article in sec_articles, f"Article with slug ''{article.slug}'' is not in second response!!"

    @staticmethod
    def check_dates_are_equal(first_date, sec_date):
        print("Checking dates are equal...")
        assert first_date == sec_date, f"Date {first_date} != {sec_date}!!"

    @staticmethod
    def check_authors_are_equal(author, expected_author):
        print("Checking authors are equal...")
        assert author == expected_author, f"Author {author} != {expected_author}!!"

    @staticmethod
    def check_slugs_are_equal(slug, expected_slug):
        print("Checking slugs are equal...")
        assert slug == expected_slug, f"Slug {slug} != {expected_slug}!!"

    @classmethod
    def check_favorited(cls, article, expected):
        print("Checking flag favorited in response...")
        favorited = article.favorited
        assert favorited is expected, f"Article with slug '{article.slug}' was {'not ' if not expected else ''} added to Favorites"

    @classmethod
    def check_article_was_added_to_favorites(cls, slug, token):
        print(f"Checking article with {slug} was added to favorites...")
        articles, response = articles_api.get_articles_by_slug(slug=slug, token=token)
        cls.check_favorited(articles.articles, True)

    @classmethod
    def check_article_was_deleted_from_favorites(cls, slug, token):
        print(f"Checking article with {slug} was deleted from favorites...")
        articles, response = articles_api.get_articles_by_slug(slug=slug, token=token)
        cls.check_favorited(articles.articles, False)

    @classmethod
    def check_comments_are_equal(cls, comment, expected_comment):
        print(f"Checking articles comments ''{comment}'' and ''{expected_comment}'' are equal...")
        assert comment == expected_comment, f"Comment {comment} is not equal {expected_comment}"

    @classmethod
    def check_comment_was_deleted(cls, slug, token):
        print(f"Checking comments for article ''{slug}'' was deleted")
        comments, _ = articles_api.get_article_comments(slug=slug, token=token)
        for comment in comments.comments:
            assert comment is None, f"Comment for article ''{slug}'' was not deleted!!"


