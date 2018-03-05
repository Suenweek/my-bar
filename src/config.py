import os
import tempfile

APP_NAME = "my-bar"
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(SRC_DIR)
RESOURCES_DIR = os.path.join(APP_DIR, "resources")
TMP_DIR = tempfile.gettempdir()
DATABASE_NAME = "{}.db".format(APP_NAME)
DATABASE_URL = "sqlite:///{}".format(
    os.path.join(RESOURCES_DIR, DATABASE_NAME)
)
