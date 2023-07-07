
from typing import Any, Optional
from dataclasses import dataclass
from pydantic import BaseModel
from generators.generator import TestDataGenerator


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


class UserRequestParams(BaseModel):
    email: Optional[str] = TestDataGenerator.generate_user_data()[0]
    password: Optional[str] = TestDataGenerator.generate_user_data()[1]
    username: Optional[str] = TestDataGenerator.generate_user_data()[2]


class UserRequest(BaseModel):
    user: UserRequestParams = UserRequestParams()


def test_register_user():
    request_body = UserRequest()
    print(request_body.model_dump_json())
