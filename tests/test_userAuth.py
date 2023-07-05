import pytest
from src.API.auth_api import AuthAPI
from src.helpers.file_worker import FileWorker
from src.helpers.user_test_data import UserTestData
fileworker = FileWorker


# from src.models.user import User
#
# auth_api = AuthAPI
#
#
# @pytest.mark.order(1)
# def test_register_user():
#     random_user = User(isRandom=True)
#     response = AuthAPI.register_user(random_user)
#     print(response.text)
#
#
@pytest.mark.order(2)
def test_user_login():
    registered_user = UserTestData(False)
    user = AuthAPI.login_user(registered_user)
    print(user.token)

@pytest.mark.order(2)
def test_update_user():
    registered_user = UserTestData(False)
    user = AuthAPI.login_user(registered_user)
    token = user.token
    print(f'Email авторизованного пользователя {user.email}')
    current_user = AuthAPI.get_current_user(token)
    print(f'Email текущего пользователя {current_user.email}')
    token = current_user.token
    new_email = UserTestData(True).email
    updated_user_email = AuthAPI.update_user(token, new_email).email
    print(updated_user_email)




