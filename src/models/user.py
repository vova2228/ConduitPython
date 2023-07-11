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


class UserRequestModel(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None

    @staticmethod
    def create_random_user():
        return UserRequestModel(
            email=TestDataGenerator.generate_email(),
            password=TestDataGenerator.generate_password(),
            username=TestDataGenerator.generate_username()
        )

    @staticmethod
    def get_user_from_file():
        user_info = FileWorker.get_user_from_file()
        return UserRequestModel(
            email=user_info[0],
            password=user_info[1],
            username=user_info[2]
        )


class UpdateUserRequestModel(BaseModel):
    email: Optional[str]

    @staticmethod
    def get_new_email():
        return UpdateUserRequestModel(
            email=TestDataGenerator.generate_email()
        )


class RequestModel(BaseModel):
    user: Union[UserRequestModel, UpdateUserRequestModel]

    def create_body(self) -> str:
        return self.model_dump_json()


class UserRequest:
    """
    Generates a user request.
    Args:
        types (RequestType): Type of request (register, login, update)
        is_random (bool): Whether to generate random or read from file
    """

    def __init__(self, types: RequestType, is_random: bool = True):
        if types == RequestType.update:
            self.body = RequestModel(user=UpdateUserRequestModel.get_new_email()).create_body()
        if types == RequestType.register or types == RequestType.login:
            if is_random:
                self.body = RequestModel(user=UserRequestModel.create_random_user()).create_body()
            else:
                self.body = RequestModel(user=UserRequestModel.get_user_from_file()).create_body()
