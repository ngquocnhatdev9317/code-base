import os

from dotenv import load_dotenv

load_dotenv()

SCHEMA = os.getenv("PG_SCHEMA", "")
HOST = os.getenv("PG_HOST", "")
PORT = os.getenv("PG_PORT", "")
USER = os.getenv("PG_USER", "")
PASSWORD = os.getenv("PG_PASSWORD", "")
URL = os.getenv("PG_URL", "")
