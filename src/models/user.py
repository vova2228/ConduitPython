from dataclasses import dataclass
from src.generators.generator import TestDataGenerator
from src.utils.utils import Utils


@dataclass
class User:
    isRandom: bool

    def __post_init__(self):
        if self.isRandom:
            self.email, self.password, self.username = TestDataGenerator.generate_user_data()
        else:
            self.email, self.password, self.username = Utils.read_user_data()
