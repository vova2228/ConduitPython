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
    with step("Get user from file"):
        global user
        user = utils.get_user(RequestType.login, is_random=False)


@allure.suite("Authorization tests")
@allure.title("Updating a user's email")
@pytest.mark.order(7)
def test_update_user():
    with step("Log in"):
        login_user, response = auth_api.login_user(user)
        token = login_user.token

    with step("Generate a new email and bio"):
        user_for_update = utils.get_user(RequestType.update)

    with step("Update the user"):
        updated_user, response = auth_api.update_user(token, user_for_update)

    with step("Check that the response body has the correct data"):
        tests.check_res_body_username(login_user, updated_user)
        tests.check_auth_response(
            response, SuccesfullRegistration.expected_keys, SuccesfullRegistration.status_code)
