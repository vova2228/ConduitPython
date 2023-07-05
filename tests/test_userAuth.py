import pytest
from src.API.auth_api import AuthAPI
from src.helpers.file_worker import FileWorker
from src.helpers.helper import Helper
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
    print(registered_user.email)
    user = AuthAPI.login_user(registered_user)
    print(user.token)
    #TODO Сделать один файл для зарегннах пользователей а другой для только что регистрируемых







