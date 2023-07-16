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
@allure.title("Getting the current user after authorization")
@pytest.mark.order(5)
def test_get_current_user_after_login():
    with step("Log in"):
        login_user, response = AuthAPI().login_user(user)
        token = login_user.token

    with step("Get current user by token"):
        current_user, response = AuthAPI().get_current_user(token)

    with step("Check that the response body has the correct data"):
        AuthCheck().check_auth_res_body(login_user, current_user)
        AuthCheck().check_auth_response(
            response, SuccesfullRegistration.expected_keys,
            SuccesfullRegistration.status_code)
