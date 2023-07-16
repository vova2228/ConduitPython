import allure
import pytest
from src.models.user import UserRequest
from src.API.authorization_api.auth_api import AuthAPI
from src.API.authorization_api.request_type import RequestType
from src.expected_results.auth_expected_results import *
from src.utils.utils import Utils
from tests.authorization.auth_check import AuthCheck

step = allure.step
user: UserRequest


def setup_function():
    with step("Get user from file"):
        global user
        user = Utils.get_user(RequestType.login, is_random=False)


@allure.suite("Authorization tests")
@allure.title("Authorization of a registered user")
@pytest.mark.order(3)
def test_old_user_login():
    with step("Log in"):
        login_user, response = AuthAPI().login_user(user)

    with step("Check that the response body has the correct data"):
        AuthCheck().check_auth_response(response, SuccesfullLogin.expected_keys, SuccesfullLogin.status_code)
