from dataclasses import dataclass
from typing import Any, List, Optional, Union
from pydantic import BaseModel
from src.helpers.file_worker import FileWorker


@dataclass
class Author:
    username: str
    bio: str
    image: str
    following: bool

    @staticmethod
    def from_dict(obj: Any) -> 'Author':
        _username = str(obj.get("username"))
        _bio = str(obj.get("bio"))
        _image = str(obj.get("image"))
        _following = bool(obj.get("following"))
        return Author(_username, _bio, _image, _following)


@dataclass
class Article:
    slug: str
    title: str
    description: str
    body: str
    tagList: str
    createdAt: str
    updatedAt: str
    favorited: bool
    favoritesCount: int
    author: Author

    @staticmethod
    def from_dict(obj: Any) -> 'Article':
        _slug = str(obj.get("slug"))
        _title = str(obj.get("title"))
        _description = str(obj.get("description"))
        _body = str(obj.get("body"))
        _tagList = str(obj.get("tagList"))
        _createdAt = str(obj.get("createdAt"))
        _updatedAt = str(obj.get("updatedAt"))
        _favorited = bool(obj.get("favorited"))
        _favoritesCount = int(obj.get("favoritesCount"))
        _author = Author.from_dict(obj.get("author"))
        return Article(
            _slug, _title, _description, _body, _tagList, _createdAt, _updatedAt, _favorited,
            _favoritesCount, _author)


@dataclass
class ArticleBody:
    articles: Union[List[Article], Article]
    articlesCount: int | None

    @staticmethod
    def from_dict(obj: Any) -> 'ArticleBody':
        if isinstance(obj.get("articles"), list):
            articles = [Article.from_dict(article) for article in obj.get("articles")]
        else:
            articles = Article.from_dict(obj.get("article"))
        articlesCount = obj.get("articlesCount")
        if articlesCount is not None:
            articlesCount = int(articlesCount)
        return ArticleBody(articles, articlesCount)


class ArticleText(BaseModel):
    title: Optional[str]
    description: Optional[str]
    body: Optional[str]
    tagList: Optional[List[str]]

    @staticmethod
    def get_article_from_file():
        article_info = FileWorker.get_article_from_file()
        return ArticleText(
            title=article_info[0],
            description=article_info[1],
            body=article_info[2],
            tagList=article_info[3]
        )


class ArticleRequestBody(BaseModel):
    article: Optional[ArticleText] = ArticleText.get_article_from_file()

    def create_body(self) -> str:
        return self.model_dump_json()
