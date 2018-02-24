import os


APP_NAME = "my-bar"
APP_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(APP_DIR, "resources")
DATABASE_NAME = "{}.db".format(APP_NAME)
DATABASE_URL = "sqlite:///{}".format(
    os.path.join(RESOURCES_DIR, DATABASE_NAME)
)
