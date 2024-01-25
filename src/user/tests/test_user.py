import json
from typing import Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession

from conftest import BaseTestCase, get_postgres_container
from database.connection import Connection
from user.schemas.user_schema import UserSchema


class TestUser(BaseTestCase):
    async def set_up_user(self) -> Coroutine[Any, Any, None]:
        conn = Connection(engine=get_postgres_container())
        async with AsyncSession(conn.engine, expire_on_commit=False) as session:
            user = UserSchema(many=True).load(
                [
                    {
                        "name": f"username{i+1}",
                        "email": f"username{i+1}@email.com",
                        "password": "abc",
                    }
                    for i in range(10)
                ],
                session=session,
            )
            session.add_all(user)
            await session.commit()
            await session.aclose()
        await conn.engine.dispose()

    async def test_user_api_get(self):
        await self.set_up_user()
        request = self.client.get("/user")
        response = await request
        response_json = await response.json()

        self.assertEqual(response.status, 200)
        self.assertEqual(response_json["status"], True)
        self.assertEqual(response_json["status_code"], 200)
        self.assertEqual(len(response_json["result"]), 10)

    async def test_user_api_post(self):
        request = self.client.post(
            "/user",
            data=json.dumps(
                {
                    "name": "usernameTest",
                    "email": "emailTest@email.com",
                    "password": "abc",
                }
            ),
        )
        response = await request
        response_json = await response.json()

        self.assertEqual(response.status, 201)
        self.assertEqual(response_json["status"], True)
        self.assertEqual(response_json["status_code"], 200)

    async def test_heath_check_api(self):
        request = self.client.get("/user")
        response = await request

        self.assertEqual(response.status, 200)
