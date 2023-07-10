from requests import Response
from tests.baseTest import BaseTest


class ArticlesTests(BaseTest):

    @classmethod
    def check_articles_response(cls, response: Response, expected_text: list | str, expected_status_code):
        print("Проверяем тело ответа...")
        if isinstance(expected_text, list):
            for key in expected_text:
                assert key in response.text, f"Ответ сервера не содержит ключ {key}!!"
        else:
            assert expected_text in response.text, f"Ответ сервера не содержит текст {expected_text}!!"

        assert response.status_code == expected_status_code, f"Статус код ответа от сервера = {response.status_code} вместо {expected_status_code}!!"

    @classmethod
    def check_response_article_count(cls, expected_count, actual_count):
        print(f"Проверяем, что число запрошенных статей {expected_count} = числу полученных статей {actual_count}")
        assert expected_count == actual_count, f"Количество статей в ответе должно быть равно {expected_count}, но кол-во = {actual_count}"