import os

from requests import Response
from src.Clients.base_client import BaseClient


class AuthApiClient(BaseClient):
    __base_url = os.environ.get("BASE_URL")
    __auth_register_path = os.environ.get("auth_register_path")
    __auth_login_path = os.environ.get("auth_login_path")
    __auth_current_user_path = os.environ.get("auth_current_user_path")

    __register_endpoint = f'{__base_url}{__auth_register_path}'
    __login_endpoint = f'{__base_url}{__auth_login_path}'
    __current_user_endpoint = f'{__base_url}{__auth_current_user_path}'

    __client = BaseClient()

    def register(self, request_body=None, request_headers=None) -> Response:
        response = self.__client.custom_request("POST", self.__register_endpoint, json=request_body)
        return response

    def login(self, request_body=None, request_headers=None) -> Response:
        response = self.__client.custom_request("POST", self.__login_endpoint, json=request_body)
        return response

    def get_user(self, request_body=None, request_headers=None) -> Response:
        response = self.__client.custom_request("GET", self.__current_user_endpoint, headers=request_headers)
        return response

    def update_user(self, request_body=None, request_headers=None) -> Response:
        response = self.__client.custom_request("PUT", self.__current_user_endpoint, headers=request_headers, json=request_body)
        return response
