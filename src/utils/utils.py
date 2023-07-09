import random


class Utils:

    @staticmethod
    def get_random_article(articles):
        if not articles:
            return None
        return articles[random.randint(0, len(articles) - 1)]
