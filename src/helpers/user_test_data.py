from src.generators.generator import TestDataGenerator
from src.utils.utils import Utils
from dataclasses import dataclass


@dataclass
class UserTestData:
    isRandom: bool

    def __post_init__(self):
        if self.isRandom:
            self.email, self.password, self.username = TestDataGenerator.generate_user_data()
        else:
            self.email, self.password, self.username = Utils.get_user_from_file()
