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


@allure.suite("Тесты авторизации")
class TestAuth:

    @allure.title("Регистрация нового пользователя")
    @pytest.mark.order(1)
    def test_new_user_register(self):
        with step("Генерируем рандомного пользователя"):
            user = utils.get_user(RequestType.register, is_random=True)

        with step("Регистрируем пользователя"):
            registered_user, response = auth_api.register_user(user)

        with step("Проверяем, что тело ответа в формате JSON"):
            tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            tests.check_auth_response(
                response, SuccesfullRegistration.expected_keys,
                SuccesfullRegistration.status_code)

    @allure.title("Попытка регистрации уже зарегистрированного пользователя")
    @pytest.mark.order(2)
    def test_old_user_register(self):
        with step("Получаем пользователя из файла"):
            user = utils.get_user(RequestType.register, is_random=False)

        with step("Пытаемся зарегистрировать пользователя"):
            registered_user, response = auth_api.register_user(user)

        with step("Проверяем, что тело ответа в формате JSON"):
            tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            tests.check_auth_response(
                response, RegistrationDataAlreadyBeenTaken.expected_text,
                RegistrationDataAlreadyBeenTaken.status_code)

    @allure.title("Авторизация зарегистрированного пользователя")
    @pytest.mark.order(3)
    def test_old_user_login(self):
        with step("Получаем пользователя из файла"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Авторизуемся"):
            login_user, response = auth_api.login_user(user)

        with step("Проверяем, что тело ответа в формате JSON"):
            tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            tests.check_auth_response(response, SuccesfullLogin.expected_keys, SuccesfullLogin.status_code)

    @allure.title("Попытка авторизации незарегистрированного пользователя")
    @pytest.mark.order(4)
    def test_new_user_login(self):
        with step("Генерируем рандомного пользователя"):
            user = utils.get_user(RequestType.login, is_random=True)

        with step("Пытаемся авторизоваться"):
            login_user, response = auth_api.login_user(user)

        with step("Проверяем, что тело ответа в формате JSON"):
            tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            tests.check_auth_response(response, UserIsNotRegistered.expected_text, UserIsNotRegistered.status_code)

    @allure.title("Получение текущего пользователя после авторизации")
    @pytest.mark.order(5)
    def test_get_current_user_after_login(self):
        with step("Получаем пользователя из файла"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Авторизуемся"):
            login_user, response = auth_api.login_user(user)
            token = login_user.token

        with step("Получаем текущего пользователя по токену"):
            current_user, response = auth_api.get_current_user(token)

        with step("Проверяем, что тело ответа в формате JSON"):
            tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            tests.check_auth_res_body(login_user, current_user)
            tests.check_auth_response(
                response, SuccesfullRegistration.expected_keys,
                SuccesfullRegistration.status_code)

    @allure.title("Получение текущего пользователя после регистрации")
    @pytest.mark.order(6)
    def test_get_current_user_after_register(self):
        with step("Генерируем рандомного пользователя"):
            user = utils.get_user(RequestType.register, is_random=True)

        with step("Регистрируем пользователя"):
            registered_user, response = auth_api.register_user(user)
            token = registered_user.token

        with step("Получаем текущего пользователя по токену"):
            current_user, _ = auth_api.get_current_user(token)

        with step("Проверяем, что тело ответа в формате JSON"):
            tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            tests.check_auth_res_body(registered_user, current_user)
            tests.check_auth_response(
                response, SuccesfullRegistration.expected_keys,
                SuccesfullRegistration.status_code)

    @allure.title("Обновление email пользователя")
    @pytest.mark.order(7)
    def test_update_user(self):
        with step("Получаем пользователя из файла"):
            user = utils.get_user(RequestType.login, is_random=False)

        with step("Авторизуемся"):
            login_user, response = auth_api.login_user(user)
            token = login_user.token

        with step("Генерируем новый email"):
            user_for_update = utils.get_user(RequestType.update)

        with step("Обновляем пользователя"):
            updated_user, response = auth_api.update_user(token, user_for_update)

        with step("Проверяем, что тело ответа в формате JSON"):
            tests.check_response_is_json(response)

        with step("Проверяем, что тело ответа имеет корректные данные"):
            tests.check_res_body_username(login_user, updated_user)
            tests.check_auth_response(
                response, SuccesfullRegistration.expected_keys, SuccesfullRegistration.status_code)
