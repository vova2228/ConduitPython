from typing import Any, Optional, Union
from dataclasses import dataclass
from pydantic import BaseModel
from generators.generator import TestDataGenerator
from helpers.file_worker import FileWorker


@dataclass
class User:
    email: str
    username: str
    bio: str
    image: str
    token: str

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        _email = str(obj.get("email"))
        _username = str(obj.get("username"))
        _bio = str(obj.get("bio"))
        _image = str(obj.get("image"))
        _token = str(obj.get("token"))
        return User(_email, _username, _bio, _image, _token)


class RandomUser(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None

    @staticmethod
    def create_random_user():
        return RandomUser(
            email=TestDataGenerator.generate_email(),
            password=TestDataGenerator.generate_password(),
            username=TestDataGenerator.generate_username()
        )


class RegisteredUser(BaseModel):
    email: Optional[str]
    password: Optional[str]
    username: Optional[str]

    @staticmethod
    def get_user_from_file():
        return RegisteredUser(
            email=FileWorker.get_user_from_file()[0],
            password=FileWorker.get_user_from_file()[1],
            username=FileWorker.get_user_from_file()[2]
        )


class Request(BaseModel):
    user: Union[RandomUser, RegisteredUser]

    def create_body(self) -> str:
        return self.model_dump_json()


class UserRequest:
    def __init__(self, is_random: bool):
        if is_random:
            self.body = Request(user=RandomUser.create_random_user()).create_body()
        else:
            self.body = Request(user=RegisteredUser.get_user_from_file()).create_body()
