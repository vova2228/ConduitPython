import os

from requests import Response
from src.Clients.base_client import BaseClient


class ArticlesClient(BaseClient):
    __base_url = os.environ.get("BASE_URL")
    __get_articles_path = os.environ.get("get_articles_path")
    __post_articles_path = os.environ.get("post_articles_path")

    __get_articles_endpoint = f'{__base_url}{__get_articles_path}'
    __post_articles_endpoint = f'{__base_url}{__post_articles_path}'

    __client = BaseClient()

    def get_articles(self, request_headers=None, **kwargs) -> Response:
        query_params = None
        if "limit" in kwargs and "offset" in kwargs:
            query_params = {"limit": kwargs.get("limit"), "offset": kwargs.get("offset")}
        elif "tag" in kwargs:
            query_params = {"tag": kwargs.get("tag"), "limit": kwargs.get("limit")}
        elif "author" in kwargs:
            query_params = {"author": kwargs.get("author")}

        headers = request_headers
        response = self.__client.custom_request("GET", self.__get_articles_endpoint, headers=headers, params=query_params)
        return response

    def post_article(self, request_body=None, request_headers=None):
        response = self.__client.custom_request(
            "POST", self.__get_articles_endpoint, headers=request_headers, json=request_body)
        return response

    def delete_article(self, slug, request_body=None, request_headers=None):
        response = self.__client.custom_request(
            "DELETE", f'{self.__get_articles_endpoint}/{slug}', headers=request_headers)
        return response
