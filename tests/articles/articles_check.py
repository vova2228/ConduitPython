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
        assert first_articles != sec_articles, "First articles response is equal sec article response!!"

    @staticmethod
    def check_articles_are_equal(first_articles: list, sec_articles: list):
        for article in first_articles:
            assert article in sec_articles, f"Article with slug ''{article.slug}'' is not in second response!!"
