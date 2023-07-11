from requests import Response
from tests.baseTest import BaseTest


class ArticlesTests(BaseTest):

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

        assert response.status_code == expected_status_code, f"The status code of the response from the server = {response.status_code} instead of {expected_status_code}!!"

    @classmethod
    def check_response_article_count(cls, expected_count, actual_count):

        """
        Checks that the number of articles in an API response matches an expected count.

        Args:
            expected_count (int): The expected number of articles in the response.
            actual_count (int): The actual number of articles in the response.
        """

        print(f"Check that the number of requested articles {expected_count} = the number of received articles {actual_count}")
        assert expected_count == actual_count, f"The number of articles in the response should be equal to {expected_count}, but the number = {actual_count}"