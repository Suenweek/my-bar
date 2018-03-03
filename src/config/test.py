from .default import *

DATABASE_URL = "sqlite:///{}".format(
    os.path.join(TMP_DIR, DATABASE_NAME)
)
