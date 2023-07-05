import os
from src.Clients.base_client import BaseClient
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

    @classmethod
    def register_user(cls, user) -> User:
        email, password, username = user.email, user.password, user.username
        request_body = {
            "user": {
                "email": email,
                "password": password,
                "username": username
            }
        }
        response = cls.__client.custom_request("POST", cls.__register_endpoint, json=request_body)
        response_body = response.json()['user']
        registered_user = User.from_dict(response_body)
        return registered_user

    @classmethod
    def login_user(cls, user) -> User:
        email, password = user.email, user.password
        request_body = {
            "user": {
                "email": email,
                "password": password
            }
        }
        response = cls.__client.custom_request("POST", cls.__login_endpoint, json=request_body)
        response_body = response.json()['user']
        authorized_user = User.from_dict(response_body)
        return authorized_user

    @classmethod
    def get_current_user(cls, token) -> User:
        headers = {"Authorization": f'Token {token}'}
        response = cls.__client.custom_request("GET", cls.__current_user_endpont, headers=headers)
        response_body = response.json()['user']
        current_user = User.from_dict(response_body)
        return current_user

    @classmethod
    def update_user(cls, token, new_email) -> User:
        headers = {"Authorization": f'Token {token}'}

        request_body = {
            "user": {
                "email": new_email
            }
        }

        response = cls.__client.custom_request("PUT", cls.__current_user_endpont, headers=headers, json=request_body)
        response_body = response.json()['user']
        current_user = User.from_dict(response_body)
        # TODO подумать куда записывать обновленный email
        return current_user
