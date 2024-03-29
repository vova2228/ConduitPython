from requests import Response
from src.models.user import UserBody
from tests.basic_check import BaseCheck


class AuthCheck(BaseCheck):

    @classmethod
    def check_auth_response(cls, response: Response, expected_text: list | str, expected_status_code):
        print("Checking the response body...")
        if isinstance(expected_text, list):
            for key in expected_text:
                assert key in response.text, f"The server response does not contain the key {key}!!"
        else:
            assert expected_text in response.text, f"The server response does not contain the text {expected_text}!!"

        cls.check_status_code(response, expected_status_code)
        cls.check_response_is_json(response)

    @classmethod
    def check_auth_res_body(cls, first_user: UserBody, sec_user: UserBody):
        print("Checking the response body...")
        cls.check_res_body_email(first_user, sec_user)
        cls.check_res_body_username(first_user, sec_user)

    @classmethod
    def check_res_body_username(cls, first_user: UserBody, sec_user: UserBody):
        print(f"Check that {first_user.username} == {sec_user.username}")
        assert first_user.username == sec_user.username, f"The username of the first user {first_user.username} is not equal to the username of the second {sec_user.username}"

    @classmethod
    def check_res_body_email(cls, first_user: UserBody, sec_user: UserBody):
        print(f"Check that {first_user.email} == {sec_user.email}")
        assert first_user.email == sec_user.email, f"The email of the first user {first_user.email} is not equal to the email of the second {sec_user.email}"
