from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DataBase(object):

    def __init__(self, url):
        self.engine = create_engine(url)
        self.session_class = sessionmaker(bind=self.engine)

    @property
    @contextmanager
    def session(self):
        session = self.session_class()
        try:
            yield session
        except Exception:
            session.rollback()
        finally:
            session.close()


def create_db(config):
    return DataBase(config.DATABASE_URL)
