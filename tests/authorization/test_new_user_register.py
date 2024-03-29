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
@allure.title("Registering a new user")
@pytest.mark.order(1)
def test_new_user_register():
    with step("Register user"):
        registered_user, response = AuthAPI().register_user(user)

    with step("Check that the response body has the correct data"):
        AuthCheck().check_auth_response(
            response, SuccesfullRegistration.expected_keys,
            SuccesfullRegistration.status_code)
