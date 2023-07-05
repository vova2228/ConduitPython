import random
from src.helpers.file_worker import FileWorker

fileworker = FileWorker


class Utils:

    @staticmethod
    def get_user_from_file():
        sheet = fileworker.initialize_sheet()
        filled_rows = fileworker.count_filled_rows(sheet)

        if filled_rows != 1:
            index = random.randint(1, filled_rows)
        else:
            index = 1

        email = sheet[f'A{index}'].value
        password = sheet[f'B{index}'].value
        username = sheet[f'C{index}'].value

        return email, password, username
