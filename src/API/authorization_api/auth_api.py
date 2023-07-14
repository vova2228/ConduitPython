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
        print("\nRegistering a user...")
        request_body = json.loads(user.body)
        response = self.__client.register(request_body)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            registered_user = self.__deserializer.deserialize(response.json()['user'], UserBody)
            if type(registered_user) is UserBody:
                print("User registered\n")
                return registered_user, response
        except KeyError:
            print("User was not registered\n")
            return None, response

    def login_user(self, user: UserRequest) -> tuple[Optional[UserBody], Response]:
        print("\nLogging in...")
        request_body = json.loads(user.body)
        response = self.__client.login(request_body)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            authorized_user: UserBody = self.__deserializer.deserialize(response.json()['user'], UserBody)
            print("User authorized\n")
            return authorized_user, response
        except KeyError:
            print("User was not authorized\n")
            return None, response

    @classmethod
    def get_current_user(cls, token) -> tuple[Optional[UserBody], Response]:
        print("\nGetting the current user...")
        headers = {"Authorization": f'Token {token}'}
        response = cls.__client.get_user(request_headers=headers)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            current_user = cls.__deserializer.deserialize(response.json()['user'], UserBody)
            print("User received\n")
            return current_user, response
        except KeyError:
            print("User was not authorized")
            return None, response

    def update_user(self, token, user: UserRequest) -> tuple[Optional[UserBody], Response]:
        print("\nUpdating the user...")
        headers = {"Authorization": f'Token {token}'}
        request_body = json.loads(user.body)
        old_email = self.get_current_user(token)[0].email
        old_bio = self.get_current_user(token)[0].bio
        response = self.__client.update_user(request_body, request_headers=headers)
        allure.attach(str(response.text), 'response', allure.attachment_type.TEXT)
        try:
            user = self.__deserializer.deserialize(response.json()['user'], UserBody)
            print("User Updated\n")
            was_updated = FileWorker.insert_new_email_and_bio_for_user(old_email, request_body['user']['email'],
                                                                       old_bio, request_body['user']['bio'])
            if was_updated:
                print(f"The user's email {old_email} in the file was updated to {request_body['user']['email']}\n")
            else:
                print(f"Email {old_email} not found in file\n")
            return user, response
        except KeyError:
            print("User was not updated")
            return None, response
