from src.generators.generator import TestDataGenerator
from src.helpers.file_worker import FileWorker
from dataclasses import dataclass


@dataclass
class UserTestData:
    isRandom: bool

    def __post_init__(self):
        if self.isRandom:
            self.email, self.password, self.username = TestDataGenerator.generate_user_data()
        else:
            self.email, self.password, self.username = FileWorker.get_user_from_file()
