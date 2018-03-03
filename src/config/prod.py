from .default import *

DATABASE_URL = "sqlite:///{}".format(
    os.path.join(RESOURCES_DIR, DATABASE_NAME)
)
