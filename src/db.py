from functools import wraps
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base


Session = sessionmaker()


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def with_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            kwargs.update(session=session)
            return f(*args, **kwargs)
    return wrapper


class GetOrCreateMixin(object):

    @classmethod
    def get_one_or_create(model, session, **kwargs):
        try:
            return session.query(model).filter_by(**kwargs).one()
        except NoResultFound:
            instance = model(**kwargs)
            session.add(instance)
            session.flush()
            return instance


class DeclarativeBase(GetOrCreateMixin):
    """In case one wants to add more mixins."""


Base = declarative_base(cls=DeclarativeBase)


class DataBase(object):

    def __init__(self, url):
        self.engine = create_engine(url)
        Session.configure(bind=self.engine)

    def create_all(self):
        Base.metadata.create_all(self.engine)

    def drop_all(self):
        Base.metadata.drop_all(self.engine)
