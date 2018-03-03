import pytest
from click.testing import CliRunner
from src.db import DataBase
from src.app import App


@pytest.fixture()
def db():
    db = DataBase(url="sqlite:///:memory:")
    db.create_all()

    yield db

    db.drop_all()


@pytest.fixture(scope="class")
def app():
    app = App(env="test")
    app.db.create_all()

    yield app

    app.db.drop_all()


@pytest.fixture(scope="module")
def cli_runner():
    runner = CliRunner(env={"MY_BAR_ENV": "test"})

    yield runner
