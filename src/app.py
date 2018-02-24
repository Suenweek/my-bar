from .db import DataBase
from .resources import Resources


class App(object):

    def __init__(self, config):
        self.config = config
        self.db = DataBase(config.DATABASE_URL)
        self.resources = Resources(config.RESOURCES_PATH)
