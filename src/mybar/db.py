from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base


class DeclarativeBase(object):

    @classmethod
    def get_one_or_create(model, session, **kwargs):
        try:
            return session.query(model).filter_by(**kwargs).one()
        except NoResultFound:
            instance = model(**kwargs)
            session.add(instance)
            session.flush()
            return instance


Base = declarative_base(cls=DeclarativeBase)


class DataBase(object):

    def __init__(self, url):
        self.engine = create_engine(url)
        self.Session = sessionmaker()

    @contextmanager
    def session_scope(self):
        session = self.Session(bind=self.engine)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def create_all(self):
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        Base.metadata.drop_all(self.engine)
