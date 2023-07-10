import json
from typing import Optional

import allure
from requests import Response
from src.Clients.auth_api_client import AuthApiClient
from src.helpers.deserializer import Deserializer
from src.helpers.file_worker import FileWorker
from src.models.user import UserBody, UserRequest


class AuthAPI:
    __client = AuthApiClient()
    __deserializer = Deserializer()

    @classmethod
    def register_user(cls, user: UserRequest) -> tuple[Optional[UserBody], Response]:
        print("\nРегистрируем пользователя...")
        request_body = json.loads(user.body)
        response = cls.__client.register(request_body)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            registered_user = cls.__deserializer.deserialize(response.json()['user'], UserBody)
            if type(registered_user) is UserBody:
                print("Пользователь зарегистрирован\n")
                return registered_user, response
        except KeyError:
            print("Пользователь не был зарегистрирован\n")
            return None, response

    @classmethod
    def login_user(cls, user: UserRequest) -> tuple[Optional[UserBody], Response]:
        print("\nЛогинимся...")
        request_body = json.loads(user.body)
        response = cls.__client.login(request_body)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            authorized_user: UserBody = cls.__deserializer.deserialize(response.json()['user'], UserBody)
            print("Пользователь авторизован\n")
            return authorized_user, response
        except KeyError:
            print("Пользователь не был авторизован\n")
            return None, response

    @classmethod
    def get_current_user(cls, token) -> tuple[Optional[UserBody], Response]:
        print("\nПолучаем текущего пользователя...")
        headers = {"Authorization": f'Token {token}'}
        response = cls.__client.get_user(request_headers=headers)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            current_user = cls.__deserializer.deserialize(response.json()['user'], UserBody)
            print("Пользователь получен\n")
            return current_user, response
        except KeyError:
            print("Пользователь не был авторизован")
            return None, response

    @classmethod
    def update_user(cls, token, user: UserRequest) -> tuple[Optional[UserBody], Response]:
        print("\nОбновляем пользователя...")
        headers = {"Authorization": f'Token {token}'}
        request_body = json.loads(user.body)
        old_email = cls.get_current_user(token)[0].email
        response = cls.__client.updade_user(request_body, request_headers=headers)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            user = cls.__deserializer.deserialize(response.json()['user'], UserBody)
            print("Пользователь Обновлен\n")
            was_updated = FileWorker.insert_new_email_for_user(old_email, request_body['user']['email'])
            if was_updated:
                print("Email пользователя в файле обновлен\n")
            else:
                print("Email не найден в файле\n")
            return user, response
        except KeyError:
            print("Пользователь не был обновлен")
            return None, response
