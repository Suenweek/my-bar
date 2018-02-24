from .db import DataBase


class MyBar(object):

    def __init__(self, config):
        self.config = config
        self.db = DataBase(url=config.DATABASE_URL)

    def list_ingredients(self):
        raise NotImplementedError
