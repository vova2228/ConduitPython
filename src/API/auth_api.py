import os

from requests import Response
from src.Clients.base_client import BaseClient
from src.expected_results.auth import RegistrationNewUser
from src.helpers.deserializer import Deserializer
from src.helpers.file_worker import FileWorker
from src.helpers.user_test_data import UserTestData
from src.models.user import User


class AuthAPI:
    __base_url = os.environ.get("BASE_URL")
    __auth_register_path = os.environ.get("auth_register_path")
    __auth_login_path = os.environ.get("auth_login_path")
    __auth_current_user_path = os.environ.get("auth_current_user_path")

    __register_endpoint = __base_url + __auth_register_path
    __login_endpoint = __base_url + __auth_login_path
    __current_user_endpont = __base_url + __auth_current_user_path

    __client = BaseClient()
    __deserializer = Deserializer()

    @classmethod
    def register_user(cls, user: UserTestData) -> User:
        print("\nРегистрируем пользователя...")
        email, password, username = user.email, user.password, user.username
        # TODO сделать негативные и позитивные тесты для авторизации
        request_body = {
            "user": {
                "email": email if email else None,
                "password": password if password else None,
                "username": username if username else None
            }
        }
        response = cls.__client.custom_request("POST", cls.__register_endpoint, json=request_body)
        print("Пользователь зарегистрирован\n")
        cls.check_keys_in_auth_response(response)
        registered_user = cls.__deserializer.deserialize(response.json()['user'], User)
        return registered_user

    @classmethod
    def login_user(cls, user) -> User:
        print("\nЛогинимся...")
        email, password = user.email, user.password
        request_body = {
            "user": {
                "email": email,
                "password": password
            }
        }
        response = cls.__client.custom_request("POST", cls.__login_endpoint, json=request_body)
        print("Пользователь авторизован\n")
        cls.check_keys_in_auth_response(response)
        authorized_user = cls.__deserializer.deserialize(response.json()['user'], User)
        return authorized_user

    @classmethod
    def get_current_user(cls, token) -> User:
        print("\nПолучаем текущего пользователя...")
        headers = {"Authorization": f'Token {token}'}
        response = cls.__client.custom_request("GET", cls.__current_user_endpont, headers=headers)
        print("Пользователь получен\n")
        cls.check_keys_in_auth_response(response)
        current_user = cls.__deserializer.deserialize(response.json()['user'], User)
        return current_user

    @classmethod
    def update_user(cls, token, new_email) -> User:
        print("\nОбновляем пользователя...")
        headers = {"Authorization": f'Token {token}'}

        request_body = {
            "user": {
                "email": new_email
            }
        }

        old_email = cls.get_current_user(token).email
        response = cls.__client.custom_request("PUT", cls.__current_user_endpont, headers=headers, json=request_body)
        print("Пользователь Обновлен\n")
        user = cls.__deserializer.deserialize(response.json()['user'], User)
        was_updated = FileWorker.insert_new_email_for_user(old_email, new_email)
        if was_updated:
            print("\nEmail пользователя в файле обновлен\n")
        else:
            print("\nEmail не найден в файле\n")
        return user

    @classmethod
    def check_keys_in_auth_response(cls, response: Response, keys=RegistrationNewUser.expected_keys):
        for key in keys:
            assert key in response.text, f"В ответе сервера нет ключа {key}!!"

