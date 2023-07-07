import pytest
from src.API.auth_api import AuthAPI
from src.helpers.user_test_data import UserTestData

auth_api = AuthAPI
user = UserTestData(isRandom=True, has_email=True, has_password=True, has_username=True)


@pytest.mark.order(1)
def test_register_user():
    auth_api.register_user(user)

