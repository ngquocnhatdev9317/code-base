from faker import Faker
from passlib.hash import pbkdf2_sha256
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from core.configs import POSTGRES_DB, URL
from database.connection import Connection
from user.model import User

fake = Faker()


def mock_user(count=1, **kwargs):
    user_instances = []
    for _ in range(count):
        username = kwargs.get("username", fake.name().lower().replace(" ", ""))
        email = kwargs.get("email", f"{username}@email.com")
        password = kwargs.get("password", fake.password(length=10))

        user_instances.append(User(**{"username": username, "email": email, "password": pbkdf2_sha256.hash(password)}))

    conn = Connection(engine=create_engine(f"postgresql+psycopg2://{URL}/{POSTGRES_DB}"))
    with Session(conn.engine, expire_on_commit=False) as session:
        session.add_all(user_instances)
        session.commit()
        session.close()

    conn.engine.dispose()
