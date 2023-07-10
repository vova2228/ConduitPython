from requests import Response

from tests.baseTest import BaseTest
from src.models.user import UserBody


class AuthTest(BaseTest):

    @classmethod
    def check_auth_response(cls, response: Response, expected_text: list | str, expected_status_code):
        print("Проверяем тело ответа...")
        if isinstance(expected_text, list):
            for key in expected_text:
                assert key in response.text, f"Ответ сервера не содержит ключ {key}!!"
        else:
            assert expected_text in response.text, f"Ответ сервера не содержит текст {expected_text}!!"

        assert response.status_code == expected_status_code, f"Статус код ответа от сервера = {response.status_code} вместо {expected_status_code}!!"

    @classmethod
    def check_auth_res_body(cls, first_user: UserBody, sec_user: UserBody):
        print("Проверяем тело ответа...")
        cls.check_res_body_email(first_user, sec_user)
        cls.check_res_body_username(first_user, sec_user)

    @classmethod
    def check_res_body_username(cls, first_user: UserBody, sec_user: UserBody):
        print(f"Проверяем, что {first_user.username} == {sec_user.username}")
        assert first_user.username == sec_user.username, f"Username первого пользователя {first_user.username} не равен username второго {sec_user.username}"

    @classmethod
    def check_res_body_email(cls, first_user: UserBody, sec_user: UserBody):
        print(f"Проверяем, что {first_user.email} == {sec_user.email}")
        assert first_user.email == sec_user.email, f"Email первого пользователя {first_user.email} не равен Email второго {sec_user.email}"
