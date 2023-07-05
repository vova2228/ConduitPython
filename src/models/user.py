from typing import Any
from dataclasses import dataclass


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


