from src.API.auth_api import AuthAPI
from src.helpers.file_worker import FileWorker
from src.helpers.user_test_data import UserTestData

fileworker = FileWorker


class Helper:

    @classmethod
    def register_users_from_file(cls):
        sheet = fileworker.initialize_sheet()
        filled_rows = fileworker.count_filled_rows(sheet)
        i = 1
        while i <= filled_rows:
            user = UserTestData(False)
            AuthAPI.register_user(user)
            i += 1


