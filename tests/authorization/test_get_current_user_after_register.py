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
        user = Utils.get_user(RequestType.register, is_random=True)


@allure.suite("Authorization tests")
@allure.title("Getting the current user after registration")
@pytest.mark.order(6)
def test_get_current_user_after_register():
    with step("Register user"):
        registered_user, response = AuthAPI().register_user(user)
        token = registered_user.token

    with step("Get current user by token"):
        current_user, _ = AuthAPI().get_current_user(token)

    with step("Check that the response body has the correct data"):
        AuthCheck().check_auth_res_body(registered_user, current_user)
        AuthCheck().check_auth_response(
            response, SuccesfullRegistration.expected_keys,
            SuccesfullRegistration.status_code)
