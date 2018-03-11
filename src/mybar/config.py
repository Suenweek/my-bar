import os
import appdirs


APP_NAME = "mybar"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(APP_DIR, "resources")
USER_DATA_DIR = appdirs.user_data_dir(APP_NAME)
DATABASE_NAME = "{}.db".format(APP_NAME)
DATABASE_URL = "sqlite:///{}".format(
    os.path.join(USER_DATA_DIR, DATABASE_NAME)
)
