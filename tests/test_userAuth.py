import pytest
from src.API.auth_api import AuthAPI
from src.models.user import User

auth_api = AuthAPI


@pytest.mark.order(1)
def test_register_user():
    random_user = User(isRandom=True)
    response = auth_api.register_user(random_user)
    print(response.text)

@pytest.mark.order(2)
def test_user_login():
    registered_user = User(isRandom=False)
    response = AuthAPI.login_user(registered_user)
    print(response.text)
