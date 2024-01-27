from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import get_postgres_container
from database.connection import Connection
from user.schemas.user_schema import UserSchema

fake = Faker()


async def mock_user(count=1, **kwargs):
    users = []
    for _ in range(count):
        name = kwargs.get("name", fake.name().lower().replace(" ", ""))
        email = kwargs.get("email", f"{name}@email.com")
        password = kwargs.get("email", fake.password(length=10))
        users.append({"name": name, "email": email, "password": password})

    conn = Connection(engine=get_postgres_container())
    async with AsyncSession(conn.engine, expire_on_commit=False) as session:
        user_instances = UserSchema(many=True).load(users, session=session)
        session.add_all(user_instances)
        await session.commit()
        await session.aclose()

    await conn.engine.dispose()
