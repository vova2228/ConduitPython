import pytest

from models.user import UserRequest
from src.API.auth_api import AuthAPI


@pytest.mark.order(1)
def test_register_user():
    user = UserRequest(is_random=False)
    print(user)
    AuthAPI.register_user(user)

