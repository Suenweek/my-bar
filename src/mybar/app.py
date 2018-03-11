import os
from .db import DataBase
from .bl import Bartender, CookBook
from .helpers import Resources


class App(object):

    def __init__(self, config):
        self.config = config
        self.db = DataBase(self.config.DATABASE_URL)
        self.resources = Resources(self.config.RESOURCES_DIR)

        self.bartender = Bartender(app=self)
        self.cookbook = CookBook(app=self)

    def ensure_user_data_dir_exists(self):
        if not os.path.exists(self.config.USER_DATA_DIR):
            os.makedirs(self.config.USER_DATA_DIR)
