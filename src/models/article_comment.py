from typing import Any, Optional, Union, List
from dataclasses import dataclass
from pydantic import BaseModel
from src.generators.generator import TestDataGenerator


@dataclass
class CommentAuthor:
    username: str
    bio: str
    image: str
    following: bool

    @staticmethod
    def from_dict(obj: Any) -> 'CommentAuthor':
        _username = str(obj.get("username"))
        _bio = str(obj.get("bio"))
        _image = str(obj.get("image"))
        _following = bool(obj.get("following"))
        return CommentAuthor(_username, _bio, _image, _following)


@dataclass
class ArticleComment:
    id: int
    createdAt: str
    updatedAt: str
    body: str
    author: CommentAuthor

    @staticmethod
    def from_dict(obj: Any) -> 'ArticleComment':
        _id = int(obj.get("id"))
        _createdAt = str(obj.get("createdAt"))
        _updatedAt = str(obj.get("updatedAt"))
        _body = str(obj.get("body"))
        _author = CommentAuthor.from_dict(obj.get("author"))
        return ArticleComment(_id, _createdAt, _updatedAt, _body, _author)


@dataclass
class ArticleCommentBody:
    comments: Union[List[ArticleComment], ArticleComment]

    @staticmethod
    def from_dict(obj: Any) -> 'ArticleCommentBody':
        if isinstance((obj.get('comments')), list):
            comments = [ArticleComment.from_dict(comment) for comment in obj.get("comments")]
        else:
            comments = ArticleComment.from_dict(obj.get("comment"))
        return ArticleCommentBody(comments)


class CommentBody(BaseModel):
    body: Optional[str]

    @staticmethod
    def get_random_comment():
        return CommentBody(
            body=TestDataGenerator.get_random_comment()
        )


class RequestModel(BaseModel):
    comment: CommentBody

    def create_body(self) -> str:
        return self.model_dump_json()


class ArticleCommentRequest:

    def __init__(self):
        self.body = RequestModel(comment=CommentBody.get_random_comment()).create_body()
