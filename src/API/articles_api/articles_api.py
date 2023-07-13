import json
from typing import Optional
import allure
from requests import Response
from API.articles_api.request_type import RequestType
from src.models.article import ArticleBody, ArticleRequest
from src.Clients.articles_client import ArticlesClient
from src.helpers.deserializer import Deserializer


class ArticlesApi:
    __client = ArticlesClient()
    __deserializer = Deserializer()

    def get_articles(self, token=None, limit=10, offset=0) -> tuple[Optional[ArticleBody], Response]:
        if token is not None:
            print(f"\nGetting articles by token with limit = {limit} and offset = {offset}...")
            headers = {"Authorization": f'Token {token}'}
        else:
            print(f"\nGetting articles with limit = {limit} and offset = {offset}...")
            headers = {}
        response = self.__client.get_articles(request_headers=headers, limit=limit, offset=offset)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print("Article received\n")
            return articles, response
        except KeyError:
            print(f"Something went wrong. Could not get the article. Response status code = {response.status_code}")
            return None, response

    def get_articles_by_slug(self, slug, token=None) -> tuple[Optional[ArticleBody], Response]:
        if token is not None:
            print(f"\nGetting articles by token with slug = ''{slug}''...")
            headers = {"Authorization": f'Token {token}'}
        else:
            print(f"\nGetting articles with slug = {slug}...")
            headers = {}
        response = self.__client.get_articles(request_headers=headers, slug=slug)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print("Article received\n")
            return articles, response
        except KeyError:
            print(f"Something went wrong. Could not get the article. Response status code = {response.status_code}")
            return None, response

    def get_articles_by_tag(self, tag, limit) -> tuple[Optional[Optional[ArticleBody]], Response]:
        response = self.__client.get_articles(tag=tag, limit=limit)
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
        response = self.__client.get_articles(request_headers=headers, author=author)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print(f"Articles by author ''{author}'' received\n")
            return articles, response
        except KeyError:
            print(f"Something went wrong. Could not get articles by author ''{author}''. Response status code = {response.status_code}")
            return None, response

    def post_articles(self, article_data: ArticleRequest = ArticleRequest(RequestType.create), token=None) -> tuple[Optional[ArticleBody], Response]:
        if token is not None:
            print(f"\nPosting an article with a token...")
        else:
            print(f"\nPosting an article without a token...")
        headers = {"Authorization": f'Token {token}'}
        request_body = json.loads(article_data.body)
        response = self.__client.post_article(request_headers=headers, request_body=request_body)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print("Article created\n")
            return articles, response
        except KeyError:
            print(f"Something went wrong. Could not post the article. Response status code = {response.status_code}")
            return None, response

    def add_article_to_favorites(self, slug, token) -> tuple[Optional[ArticleBody], Response]:
        headers = {"Authorization": f'Token {token}'}
        response = self.__client.post_article(request_headers=headers, slug=slug)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print(f"Article with slug ''{slug}'' added to favorites")
            return articles, response
        except KeyError:
            print(f"Something went wrong. Could not add article with slug ''{slug}'' to favorites. Response status code = {response.status_code}")
            return None, response

    def delete_article_from_favorites(self, slug, token) -> tuple[Optional[ArticleBody], Response]:
        headers = {"Authorization": f'Token {token}'}
        response = self.__client.delete_article_from_favorites(slug=slug, request_headers=headers)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print(f"Article with slug ''{slug}'' deleted from favorites")
            return articles, response
        except KeyError:
            print(f"Something went wrong. Could not delete article with slug ''{slug}'' from favorites. Response status code = {response.status_code}")
            return None, response

    def update_articles(self, slug, article_data: ArticleRequest = ArticleRequest(RequestType.update), token=None) -> tuple[Optional[ArticleBody], Response]:
        if token is not None:
            print(f"\nUpdating an article ''{slug}'' with a token...")
        else:
            print(f"\nUpdating an article ''{slug}'' without a token...")
        headers = {"Authorization": f'Token {token}'}
        request_body = json.loads(article_data.body)
        response = self.__client.update_article(slug, request_headers=headers, request_body=request_body)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            articles = self.__deserializer.deserialize(response.json(), ArticleBody)
            print("Article created\n")
            return articles, response
        except KeyError:
            print(f"Something went wrong. Could not post the article. Response status code = {response.status_code}")
            return None, response

    def delete_article(self, slug, token):
        headers = {"Authorization": f'Token {token}'}
        response = self.__client.delete_article(request_headers=headers, slug=slug)
        if response.status_code in [200, 204]:
            print(f"Article ''{slug}'' deleted")
        else:
            print(f"Error deleting article {slug}: response status code = {response.status_code}")
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        return response
