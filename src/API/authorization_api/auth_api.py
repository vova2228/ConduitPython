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

    def register_user(self, user: UserRequest) -> tuple[Optional[UserBody], Response]:
        print("\nРегистрируем пользователя...")
        request_body = json.loads(user.body)
        response = self.__client.register(request_body)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            registered_user = self.__deserializer.deserialize(response.json()['user'], UserBody)
            if type(registered_user) is UserBody:
                print("Пользователь зарегистрирован\n")
                return registered_user, response
        except KeyError:
            print("Пользователь не был зарегистрирован\n")
            return None, response

    def login_user(self, user: UserRequest) -> tuple[Optional[UserBody], Response]:
        print("\nЛогинимся...")
        request_body = json.loads(user.body)
        response = self.__client.login(request_body)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            authorized_user: UserBody = self.__deserializer.deserialize(response.json()['user'], UserBody)
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

    def update_user(self, token, user: UserRequest) -> tuple[Optional[UserBody], Response]:
        print("\nОбновляем пользователя...")
        headers = {"Authorization": f'Token {token}'}
        request_body = json.loads(user.body)
        old_email = self.get_current_user(token)[0].email
        response = self.__client.update_user(request_body, request_headers=headers)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            user = self.__deserializer.deserialize(response.json()['user'], UserBody)
            print("Пользователь Обновлен\n")
            was_updated = FileWorker.insert_new_email_for_user(old_email, request_body['user']['email'])
            if was_updated:
                print(f"Email пользователя {old_email} в файле обновлен на {request_body['user']['email']}\n")
            else:
                print(f"Email {old_email} не найден в файле\n")
            return user, response
        except KeyError:
            print("Пользователь не был обновлен")
            return None, response
