import os
from appdirs import user_data_dir


APP_NAME = "my-bar"
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(SRC_DIR)
RESOURCES_DIR = os.path.join(APP_DIR, "resources")
USER_DATA_DIR = user_data_dir(APP_NAME)
DATABASE_NAME = "{}.db".format(APP_NAME)
DATABASE_URL = "sqlite:///{}".format(
    os.path.join(USER_DATA_DIR, DATABASE_NAME)
)
