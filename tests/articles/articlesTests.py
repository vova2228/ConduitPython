from requests import Response
from tests.baseTest import BaseTest


class ArticlesTests(BaseTest):

    @classmethod
    def check_auth_response(cls, response: Response, expected_text: list, expected_status_code):
        for key in expected_text:
            assert key in response.text, f"Ответ сервера не содержит ключ {key}!!"

        assert response.status_code == expected_status_code , f"Статус код ответа от сервера = {response.status_code} вместо {expected_status_code}!!"
