import allure
import pytest

from tests.authorization.authTests import AuthTest
from src.API.authorization_api.request_type import RequestType
from src.expected_results.auth_expected_results import *
from src.API.authorization_api.auth_api import AuthAPI
from src.utils.utils import Utils

step = allure.step
utils = Utils()
auth_api = AuthAPI()
tests = AuthTest()


@allure.suite("Authorization tests")
class TestAuth:

    @allure.title("Registering a new user")
    @pytest.mark.order(1)
    def test_new_user_register(self):
        with step("Generate random user"):
            user = utils.get_user(RequestType.register, is_random=True)

        with step("Register user"):
            registered_user, response = auth_api.register_user(user)

        with step("Check that the response body is in JSON format"):
            tests.check_response_is_json(response)

        with step("Check that the response body has the correct data"):
            tests.check_auth_response(
                response, SuccesfullRegistration.expected_keys,
                SuccesfullRegistration.status_code)

    @allure.title("Attempt to register an already registered user")
    @pytest.mark.order(2)
    def test_old_user_register(self):
        with step("Get user from file"):
            user = utils.get_user(RequestType.register, is_random=False)

        with step("Try to register a user"):
            registered_user, response = auth_api.register_user(user)

        with step("Check that the response body is in JSON format"):
            tests.check_response_is_json(response)

        with step("Check that the response body has the correct data"):
            tests.check_auth_response(
                response, RegistrationDataAlreadyBeenTaken.expected_text,
                RegistrationDataAlreadyBeenTaken.status_code)

    @allure.title("Authorization of a registered user")
    @pytest.mark.order(3)
    def test_old_user_login(self):
        with step("Get user from file"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Log in"):
            login_user, response = auth_api.login_user(user)

        with step("Check that the response body is in JSON format"):
            tests.check_response_is_json(response)

        with step("Check that the response body has the correct data"):
            tests.check_auth_response(response, SuccesfullLogin.expected_keys, SuccesfullLogin.status_code)

    @allure.title("Attempt to authorize an unregistered user")
    @pytest.mark.order(4)
    def test_new_user_login(self):
        with step("Generate random user"):
            user = utils.get_user(RequestType.login, is_random=True)

        with step("Try to log in"):
            login_user, response = auth_api.login_user(user)

        with step("Check that the response body is in JSON format"):
            tests.check_response_is_json(response)

        with step("Check that the response body has the correct data"):
            tests.check_auth_response(response, UserIsNotRegistered.expected_text, UserIsNotRegistered.status_code)

    @allure.title("Getting the current user after authorization")
    @pytest.mark.order(5)
    def test_get_current_user_after_login(self):
        with step("Get user from file"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Log in"):
            login_user, response = auth_api.login_user(user)
            token = login_user.token

        with step("Get current user by token"):
            current_user, response = auth_api.get_current_user(token)

        with step("Check that the response body is in JSON format"):
            tests.check_response_is_json(response)

        with step("Check that the response body has the correct data"):
            tests.check_auth_res_body(login_user, current_user)
            tests.check_auth_response(
                response, SuccesfullRegistration.expected_keys,
                SuccesfullRegistration.status_code)

    @allure.title("Getting the current user after registration")
    @pytest.mark.order(6)
    def test_get_current_user_after_register(self):
        with step("Generate random user"):
            user = utils.get_user(RequestType.register, is_random=True)

        with step("Register user"):
            registered_user, response = auth_api.register_user(user)
            token = registered_user.token

        with step("Get current user by token"):
            current_user, _ = auth_api.get_current_user(token)

        with step("Check that the response body is in JSON format"):
            tests.check_response_is_json(response)

        with step("Check that the response body has the correct data"):
            tests.check_auth_res_body(registered_user, current_user)
            tests.check_auth_response(
                response, SuccesfullRegistration.expected_keys,
                SuccesfullRegistration.status_code)

    @allure.title("Updating a user's email")
    @pytest.mark.order(7)
    def test_update_user(self):
        with step("Get user from file"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Log in"):
            login_user, response = auth_api.login_user(user)
            token = login_user.token

        with step("Generate a new email"):
            user_for_update = utils.get_user(RequestType.update)

        with step("Update the user"):
            updated_user, response = auth_api.update_user(token, user_for_update)

        with step("Check that the response body is in JSON format"):
            tests.check_response_is_json(response)

        with step("Check that the response body has the correct data"):
            tests.check_res_body_username(login_user, updated_user)
            tests.check_auth_response(
                response, SuccesfullRegistration.expected_keys, SuccesfullRegistration.status_code)
