from faker import Faker
from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import Connection, get_postgres_container
from user.model import User
from utilities.configs import POSTGRES_DB, URL

fake = Faker()


async def mock_user(count=1, **kwargs):
    user_instances = []
    for _ in range(count):
        name = kwargs.get("name", fake.name().lower().replace(" ", ""))
        email = kwargs.get("email", f"{name}@email.com")
        password = kwargs.get("password", fake.password(length=10))

        user_instances.append(User(**{"name": name, "email": email, "password": pbkdf2_sha256.hash(password)}))

    conn = Connection(engine=get_postgres_container(f"postgresql+asyncpg://{URL}/{POSTGRES_DB}"))
    async with AsyncSession(conn.engine, expire_on_commit=False) as session:
        session.add_all(user_instances)
        await session.commit()
        await session.aclose()

    await conn.engine.dispose()
