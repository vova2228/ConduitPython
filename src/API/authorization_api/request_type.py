from enum import Enum


class RequestType(Enum):
    register = "register"
    update = "update"
    login = "login"