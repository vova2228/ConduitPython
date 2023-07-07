from src.generators.generator import TestDataGenerator
from src.helpers.file_worker import FileWorker
from dataclasses import dataclass


@dataclass
class UserTestData:
    isRandom: bool = None
    has_email: bool = None
    has_password: bool = None
    has_username: bool = None

    def __post_init__(self):
        if self.isRandom is None:
            self.email, self.password, self.username = None, None, None
        if self.isRandom:
            self.email, self.password, self.username = TestDataGenerator.generate_user_data()
            if self.has_email:
                self.email = TestDataGenerator.generate_user_data()[0]
            else:
                self.email = ""

            if self.has_password:
                self.password = TestDataGenerator.generate_user_data()[1]
            else:
                self.password = ""

            if self.has_username:
                self.username = TestDataGenerator.generate_user_data()[2]
            else:
                self.username = ""

        else:
            self.email, self.password, self.username = FileWorker.get_user_from_file()
            if self.has_email:
                self.email = FileWorker.get_user_from_file()[0]
            else:
                self.email = ""

            if self.has_password:
                self.password = FileWorker.get_user_from_file()[1]
            else:
                self.password = ""

            if self.has_username:
                self.username = FileWorker.get_user_from_file()[2]
            else:
                self.username = ""
