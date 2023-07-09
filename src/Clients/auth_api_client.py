import os

from requests import Response

from src.Clients.base_client import BaseClient


class AuthApiClient(BaseClient):
    __base_url = os.environ.get("BASE_URL")
    __auth_register_path = os.environ.get("auth_register_path")
    __auth_login_path = os.environ.get("auth_login_path")
    __auth_current_user_path = os.environ.get("auth_current_user_path")

    __register_endpoint = __base_url + __auth_register_path
    __login_endpoint = __base_url + __auth_login_path
    __current_user_endpont = __base_url + __auth_current_user_path

    __client = BaseClient()

    @classmethod
    def register(cls, request_body=None, request_headers=None) -> Response:
        response = cls.__client.custom_request("POST", cls.__register_endpoint, json=request_body)
        return response

    @classmethod
    def login(cls, request_body=None, request_headers=None) -> Response:
        response = cls.__client.custom_request("POST", cls.__login_endpoint, json=request_body)
        return response

    @classmethod
    def get_user(cls, request_body=None, request_headers=None) -> Response:
        response = cls.__client.custom_request("GET", cls.__current_user_endpont, headers=request_headers)
        return response

    @classmethod
    def updade_user(cls, request_body=None, request_headers=None) -> Response:
        response = cls.__client.custom_request("PUT", cls.__current_user_endpont, headers=request_headers,
                                               json=request_body)
        return response
