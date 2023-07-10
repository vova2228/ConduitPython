import json
from typing import Optional
import allure
from requests import Response
from src.models.article import ArticleBody, ArticleRequestBody
from src.Clients.articles_client import ArticlesClient
from src.helpers.deserializer import Deserializer


class ArticlesApi:
    __client = ArticlesClient()
    __deserializer = Deserializer()

    @classmethod
    def get_articles(cls, token=None, limit=10, offset=0) -> tuple[Optional[ArticleBody], Response]:
        if token is not None:
            print(f"\nПолучаем статьи по токену с параметрами limit = {limit} и offset = {offset}...")
        else:
            print(f"\nПолучаем статьи с параметрами limit = {limit} и offset = {offset}...")
        headers = {"Authorization": f'Token {token}'}
        response = cls.__client.get_article(request_headers=headers, limit=limit, offset=offset)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = cls.__deserializer.deserialize(response.json(), ArticleBody)
            print("Статья получена\n")
            return articles, response
        except KeyError:
            print(f"Что-то пошло не так. Не смогли получить статью. Статус код ответа = {response.status_code}")
            return None, response

    @classmethod
    def post_articles(cls, token=None, article_request_body: ArticleRequestBody = ArticleRequestBody()) -> tuple[Optional[ArticleBody], Response]:
        if token is not None:
            print(f"\nПостим статью с токеном...")
        else:
            print(f"\nПостим статью без токена...")
        headers = {"Authorization": f'Token {token}'}
        request_body = json.loads(article_request_body.create_body())
        response = cls.__client.post_article(request_headers=headers, request_body=request_body)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = cls.__deserializer.deserialize(response.json(), ArticleBody)
            print("Статья создана\n")
            return articles, response
        except KeyError:
            print(f"Что-то пошло не так. Не смогли запостить статью. Статус код ответа = {response.status_code}")
            return None, response

    @classmethod
    def delete_article(cls, slug=None, token=None):
        if token is not None:
            print(f"\nУдаляем статью с токеном и slug = '{slug}'...")
        else:
            print(f"\nУдаляем статью без токена и slug = '{slug}'...")
        headers = {"Authorization": f'Token {token}'}
        response = cls.__client.delete_article(request_headers=headers, slug=slug)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        return response
