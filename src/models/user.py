from typing import Any, Optional, Union
from dataclasses import dataclass
from pydantic import BaseModel
from src.API.authorization_api.request_type import RequestType
from src.generators.generator import TestDataGenerator
from src.helpers.file_worker import FileWorker


@dataclass
class UserBody:
    email: str
    username: str
    bio: str
    image: str
    token: str

    @staticmethod
    def from_dict(obj: Any) -> 'UserBody':
        _email = str(obj.get("email"))
        _username = str(obj.get("username"))
        _bio = str(obj.get("bio"))
        _image = str(obj.get("image"))
        _token = str(obj.get("token"))
        return UserBody(_email, _username, _bio, _image, _token)


class RegisterRandomUser(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None

    @staticmethod
    def create_random_user():
        return RegisterRandomUser(
            email=TestDataGenerator.generate_email(),
            password=TestDataGenerator.generate_password(),
            username=TestDataGenerator.generate_username()
        )


class RegisterRegedUser(BaseModel):
    email: Optional[str]
    password: Optional[str]
    username: Optional[str]

    @staticmethod
    def get_user_from_file():
        user_info = FileWorker.get_user_from_file()
        return RegisterRegedUser(
            email=user_info[0],
            password=user_info[1],
            username=user_info[2]
        )


class UpdateUser(BaseModel):
    email: Optional[str]

    @staticmethod
    def get_new_email():
        return UpdateUser(
            email=TestDataGenerator.generate_email()
        )


class Request(BaseModel):
    user: Union[RegisterRandomUser, RegisterRegedUser, UpdateUser]

    def create_body(self) -> str:
        return self.model_dump_json()


class UserRequest:
    def __init__(self, types: RequestType, is_random: bool = True):
        if types == RequestType.update:
            self.body = Request(user=UpdateUser.get_new_email()).create_body()
        if types == RequestType.register or types == RequestType.login:
            if is_random:
                self.body = Request(user=RegisterRandomUser.create_random_user()).create_body()
            else:
                self.body = Request(user=RegisterRegedUser.get_user_from_file()).create_body()
