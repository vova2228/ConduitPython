import random
import string
import requests
from openpyxl import load_workbook

letters = string.ascii_lowercase
file_path = "../tests/data/registered_users.xlsx"
register_endpoint = "https://api.realworld.io/api/users"
login_endpoint = "https://api.realworld.io/api/users/login"


def initialize_sheet():
    workbook = load_workbook(filename=file_path)
    sheet = workbook.active
    return sheet


def insert_new_user_to_file(users_count: int):
    sheet = initialize_sheet()

    filled_rows = count_filled_rows(sheet)

    if filled_rows == 0:
        i = 1
        while i < users_count + 1:
            random_length = random.randint(6, 11)
            add_user_to_sheet(sheet, i, random_length)
            i += 1
    else:
        users_count += filled_rows
        i = filled_rows + 1
        while i <= users_count:
            random_length = random.randint(6, 11)
            add_user_to_sheet(sheet, i, random_length)
            i += 1

    sheet.parent.save(file_path)


def count_filled_rows(sheet=None):
    if sheet is None:
        workbook = load_workbook(filename=file_path)
        sheet = workbook.active
    filled_rows = 0
    for row in sheet.iter_rows():
        if any(cell.value for cell in row):
            filled_rows += 1
    return filled_rows


def generate_email(length):
    username = ''.join(random.choice(letters) for i in range(length))
    domain = ''.join(random.choice(letters) for i in range(length))
    email = f"{username}@{domain}.com"
    return email


def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password


def generate_username(length):
    username = ''.join(random.choice(letters) for i in range(length))
    return username


def add_user_to_sheet(sheet, index, length):
    sheet[f'A{index}'] = generate_email(length)
    sheet[f'B{index}'] = generate_password(length)
    sheet[f'C{index}'] = generate_username(length)


def register_users_from_file():
    sheet = initialize_sheet()
    filled_rows = count_filled_rows(sheet)

    registered_users = 0
    index = 1
    while index <= filled_rows:
        email = sheet[f'A{index}'].value
        password = sheet[f'B{index}'].value
        username = sheet[f'C{index}'].value
        request_body = {
            "user": {
                "email": email,
                "password": password,
                "username": username
            }
        }
        response = requests.post(register_endpoint, json=request_body)
        index += 1
        if "token" in response.text:
            registered_users += 1
    return registered_users


def clear_file():
    sheet = initialize_sheet()
    sheet.delete_rows(1, sheet.max_row)
    sheet.parent.save(file_path)


def check_users_in_file_are_registered():
    sheet = initialize_sheet()
    filled_rows = count_filled_rows(sheet)

    index = 1
    unregistered_users = 0
    while index <= filled_rows:
        email = sheet[f'A{index}'].value
        password = sheet[f'B{index}'].value
        request_body = {
            "user": {
                "email": email,
                "password": password
            }
        }
        response = requests.post(login_endpoint, json=request_body)
        assert response.status_code == 200 or response.status_code == 403
        if "is invalid" in response.text:
            unregistered_users += 1
        index += 1

    return unregistered_users


def main():
    user_input = input(
        "1 - Создать в файле новых пользователей.\n"
        "2 - Очистить файл \n"
        "3 - Проверить зарегистрированы ли пользователи в файле\n"
        "4 - Зарегистрировать пользователей из файла\n"
        "5 - Узнать количество пользователей в файле\n")

    if user_input == "1":
        user_input = input("Введите количество пользователей: ")
        insert_new_user_to_file(int(user_input))
        print("Пользователи добавлены\n")
        user_input = input("Желаете их зарегистрировать? 1 - Да, 2 - Нет\n")
        if user_input == "1":
            print("Регистрируем пользователей...\n")
            registered_users = register_users_from_file()
            print("Пользователи зарегистрированы. Кол-во зарегистрированных пользователей = ", registered_users)
        else:
            pass
    elif user_input == "2":
        clear_file()
        print("Файл очищен")
    elif user_input == "3":
        print("Проверяем зарегистрированы ли пользователи...")
        unregistered_users = check_users_in_file_are_registered()
        print("Число незарегистрированных пользователей = ", unregistered_users)
    elif user_input == "4":
        print("Регистрируем пользователей...\n")
        registered_users = register_users_from_file()
        print("Пользователи зарегистрированы. Кол-во зарегистрированных пользователей = ", registered_users)
    elif user_input == "5":
        print("Количество пользоватлей в файле: ", count_filled_rows())


if __name__ == "__main__":
    main()
