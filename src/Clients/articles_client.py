import os

from requests import Response
from src.Clients.base_client import BaseClient


class ArticlesClient(BaseClient):
    __base_url = os.environ.get("BASE_URL")
    __get_articles_path = os.environ.get("get_articles_path")
    __post_articles_path = os.environ.get("post_articles_path")

    __get_articles_endpoint = __base_url + __get_articles_path
    __post_articles_endpoint = __base_url + __post_articles_path

    __client = BaseClient()

    @classmethod
    def get_article(cls, limit, offset, request_body=None, request_headers=None) -> Response:
        query_params = {"limit": limit, "offset": offset}
        response = cls.__client.custom_request("GET", cls.__get_articles_endpoint, params=query_params)
        return response

    @classmethod
    def post_article(cls, request_body=None, request_headers=None):
        response = cls.__client.custom_request("POST", cls.__get_articles_endpoint, headers=request_headers,
                                               json=request_body)
        return response

    @classmethod
    def delete_article(cls, slug, request_body=None, request_headers=None):
        response = cls.__client.custom_request("DELETE", f'{cls.__get_articles_endpoint}/{slug}', headers=request_headers)
        return response
