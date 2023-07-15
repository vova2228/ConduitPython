import allure
import pytest

from src.API.authorization_api.auth_api import AuthAPI
from src.API.authorization_api.request_type import RequestType
from src.expected_results.auth_expected_results import *
from src.utils.utils import Utils
from tests.authorization.auth_check import AuthCheck

step = allure.step
utils = Utils()
auth_api = AuthAPI()
tests = AuthCheck()


def setup_function():
    with step("Generate random user"):
        global user
        user = utils.get_user(RequestType.register, is_random=True)


@allure.suite("Authorization tests")
@allure.title("Attempt to authorize an unregistered user")
@pytest.mark.order(4)
def test_new_user_login():
    with step("Try to log in"):
        login_user, response = auth_api.login_user(user)

    with step("Check that the response body has the correct data"):
        tests.check_auth_response(response, UserIsNotRegistered.expected_text, UserIsNotRegistered.status_code)
