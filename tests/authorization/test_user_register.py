import pytest
from src.API.auth_api import AuthAPI
from src.helpers.user_test_data import UserTestData

auth_api = AuthAPI


@pytest.mark.parametrize("new_user", [UserTestData(isRandom=True), UserTestData(isRandom=False)])
@pytest.mark.order(1)
def test_register_user(new_user):
    auth_api.register_user(new_user)


@pytest.mark.order(2)
def test_login_user():
    user = UserTestData(isRandom=False)
    auth_api.login_user(user)
