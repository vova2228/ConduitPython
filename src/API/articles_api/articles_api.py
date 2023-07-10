from typing import Optional
import allure
from requests import Response
from models.article import ArticleBody
from src.Clients.articles_client import ArticlesClient
from src.helpers.deserializer import Deserializer


class ArticlesApi:
    __client = ArticlesClient()
    __deserializer = Deserializer()

    @classmethod
    def get_articles(cls, token, limit=10, offset=0) -> tuple[Optional[ArticleBody], Response]:
        print("\nПолучаем статью по токену...")
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
