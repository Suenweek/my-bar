import pytest
from src.db import DataBase


@pytest.fixture()
def db():
    database = DataBase(url="sqlite:///:memory:")
    database.create_all()
    yield database
    database.drop_all()
