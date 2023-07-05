import random
from openpyxl import load_workbook
from src.generators.generator import TestDataGenerator


class FileWorker:
    __file_path = '../tests/data/registered_users.xlsx'

    @classmethod
    def insert_new_user_to_file(cls, users_count: int):
        workbook = load_workbook(filename=cls.__file_path)
        sheet = workbook.active

        filled_rows = cls.count_filled_rows(sheet)

        if filled_rows == 0:
            i = 1
            while i < users_count + 1:
                random_length = random.randint(6, 11)
                cls.__add_user_to_sheet(sheet, i, random_length)
                i += 1
        else:
            users_count += filled_rows
            i = filled_rows + 1
            while i <= users_count:
                random_length = random.randint(6, 11)
                cls.__add_user_to_sheet(sheet, i, random_length)
                i += 1

        workbook.save(cls.__file_path)

    @classmethod
    def count_filled_rows(cls, sheet):
        filled_rows = 0
        for row in sheet.iter_rows():
            if any(cell.value for cell in row):
                filled_rows += 1
        return filled_rows

    @classmethod
    def __add_user_to_sheet(cls, sheet, index, random_length):
        sheet[f'A{index}'] = TestDataGenerator.generate_email(random_length)
        sheet[f'B{index}'] = TestDataGenerator.generate_password(random_length)
        sheet[f'C{index}'] = TestDataGenerator.generate_username(random_length)

    @classmethod
    def initialize_sheet(cls):
        workbook = load_workbook(filename=cls.__file_path)
        sheet = workbook.active
        return sheet

    @classmethod
    def get_user_from_file(cls):
        sheet = cls.initialize_sheet()
        filled_rows = cls.count_filled_rows(sheet)

        if filled_rows != 1:
            index = random.randint(1, filled_rows)
        else:
            index = 1

        email = sheet[f'A{index}'].value
        password = sheet[f'B{index}'].value
        username = sheet[f'C{index}'].value

        return email, password, username
