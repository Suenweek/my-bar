import os
import pytest
from tempfile import gettempdir
from click.testing import CliRunner
from my_bar.db import DataBase
from my_bar.app import App
from my_bar.helpers import get_config


@pytest.fixture()
def config():
    config = get_config()
    config.DATABASE_URL = "sqlite:///{}".format(
        os.path.join(gettempdir(), config.DATABASE_NAME)
    )
    yield config


@pytest.fixture()
def db(config):
    db = DataBase(url=config.DATABASE_URL)
    db.create_all()

    yield db

    db.drop_all()


@pytest.fixture(scope="class")
def app(config):
    app = App(config=config)
    app.db.create_all()

    yield app

    app.db.drop_all()


@pytest.fixture(scope="module")
def cli_runner():
    runner = CliRunner()

    yield runner
