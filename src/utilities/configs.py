import os

from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("PG_URL", "")
SCHEMA = os.getenv("PG_SCHEMA", "dummy")
DEV = bool(os.getenv("DEV", "False") == "True")
