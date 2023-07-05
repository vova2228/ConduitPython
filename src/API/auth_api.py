from src import ENV
from src.Clients.base_client import BaseClient
from src.models.user import User


class AuthAPI:
    __url = ENV.ENV.base_url
    __register_path = ENV.ENV.auth_register_path
    __login_path = ENV.ENV.auth_login_path

    __register_endpoint = __url + __register_path
    __login_endpoint = __url + __login_path

    _client = BaseClient()

    @classmethod
    def register_user(cls, user: User):
        email, password, username = user.email, user.password, user.username
        body = {
            "user": {
                "email": email,
                "password": password,
                "username": username
            }
        }
        response = cls._client.custom_request("POST", cls.__register_endpoint, json=body)
        return response

    @classmethod
    def login_user(cls, user: User):
        email, password = user.email, user.password
        body = {
            "user": {
                "email": email,
                "password": password
            }
        }
        response = cls._client.custom_request("POST", cls.__login_endpoint, json=body)
        return response
