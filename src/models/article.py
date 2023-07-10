from dataclasses import dataclass
from typing import Any, List

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
        return Article(_slug, _title, _description, _body, _tagList, _createdAt, _updatedAt, _favorited,
                       _favoritesCount, _author)


@dataclass
class ArticleBody:
    articles: List[Article]
    articlesCount: int

    @staticmethod
    def from_dict(obj: Any) -> 'ArticleBody':
        _articles = [Article.from_dict(y) for y in obj.get("articles")]
        _articlesCount = int(obj.get("articlesCount"))
        return ArticleBody(_articles, _articlesCount)
