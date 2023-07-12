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

    def get_articles(self, auth_token=None, limit=10, offset=0) -> tuple[Optional[ArticleBody], Response]:
        if auth_token is not None:
            print(f"\nGetting articles by token with limit = {limit} and offset = {offset}...")
        else:
            print(f"\nGetting articles with limit = {limit} and offset = {offset}...")
        headers = {"Authorization": f'Token {auth_token}'}
        response = self.__client.get_article(request_headers=headers, limit=limit, offset=offset)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print("Article received\n")
            return articles, response
        except KeyError:
            print(f"Something went wrong. Could not get the article. Response status code = {response.status_code}")
            return None, response

    def get_articles_by_tag(self, tag, limit) -> tuple[Optional[Optional[ArticleBody]], Response]:
        response = self.__client.get_articles_by_tag(tag, limit)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print(f"Articles by tag '{tag}' received")
            return articles, response
        except KeyError:
            print(f"Could not get articles by tag '{tag}', status {response.status_code}")
            return None, response

    def get_articles_by_author(self, author, token) -> tuple[Optional[ArticleBody], Response]:
        headers = {"Authorization": f'Token {token}'}
        response = self.__client.get_article_by_author(author, headers)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print(f"Articles by author ''{author}'' received\n")
            return articles, response
        except KeyError:
            print(f"Something went wrong. Could not get articles by author ''{author}''. Response status code = {response.status_code}")
            return None, response

    def post_articles(self, auth_token=None, article_data: ArticleRequestBody = ArticleRequestBody()) -> tuple[Optional[ArticleBody], Response]:
        if auth_token is not None:
            print(f"\nPosting an article with a token...")
        else:
            print(f"\nPosting an article without a token...")
        headers = {"Authorization": f'Token {auth_token}'}
        request_body = json.loads(article_data.create_body())
        response = self.__client.post_article(request_headers=headers, request_body=request_body)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print("Article created\n")
            return articles, response
        except KeyError:
            print(f"Something went wrong. Could not post the article. Response status code = {response.status_code}")
            return None, response

    def delete_article(self, slug=None, token=None):
        headers = {"Authorization": f'Token {token}'}
        response = self.__client.delete_article(request_headers=headers, slug=slug)
        if response.status_code in [200, 204]:
            print(f"Article ''{slug}'' deleted")
        else:
            print(f"Error deleting article {slug}: response status code = {response.status_code}")
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        return response
