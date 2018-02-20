from .db import create_db
from .models import Base


class MyBar(object):

    def __init__(self, config):
        self.config = config
        self.db = create_db(config=config)

    def create_db(self):
        Base.metadata.create_all(self.db.engine)

    def list_ingredients(self):
        raise NotImplementedError
