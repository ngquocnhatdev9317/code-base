from faker import Faker
from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import settings
from database.connection import Connection, get_postgres_container
from user.model import User

fake = Faker()


async def mock_user(count=1, **kwargs):
    user_instances = []
    for _ in range(count):
        username = kwargs.get("username", fake.name().lower().replace(" ", ""))
        email = kwargs.get("email", f"{username}@email.com")
        password = kwargs.get("password", fake.password(length=10))

        user_instances.append(User(**{"username": username, "email": email, "password": pbkdf2_sha256.hash(password)}))

    conn = Connection(engine=get_postgres_container(f"postgresql+asyncpg://{settings.url}/{settings.postgres_db}"))
    async with AsyncSession(conn.engine, expire_on_commit=False) as session:
        session.add_all(user_instances)
        await session.commit()
        await session.aclose()

    await conn.engine.dispose()
