import os

from requests import Response
from src.Clients.base_client import BaseClient


class ArticlesClient(BaseClient):
    __base_url = os.environ.get("BASE_URL")
    __get_articles_path = os.environ.get("get_articles_path")

    __get_articles_endpoint = __base_url + __get_articles_path

    __client = BaseClient()

    @classmethod
    def get_article(cls, limit, offset, request_body=None, request_headers=None) -> Response:
        query_params = {"limit": limit, "offset": offset}
        response = cls.__client.custom_request("GET", cls.__get_articles_endpoint, params=query_params)
        return response
