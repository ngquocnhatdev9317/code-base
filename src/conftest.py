import asyncio
import json
from typing import Any, Coroutine

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import Application
from sqlalchemy_utils import create_database, database_exists, drop_database

from database.base_model import BaseModel
from database.connection import get_postgres_container
from main import create_app
from tests.mockup import mock_user
from utilities.configs import POSTGRES_DB, URL

url_asyncpg = f"postgresql+asyncpg://{URL}/{POSTGRES_DB}"
url_psycopg = url_asyncpg.replace("asyncpg", "psycopg2")


async def run_init():
    engine = get_postgres_container(url_asyncpg)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)
    await engine.dispose()


def run_tear_down():
    drop_database(url_psycopg)


class BaseTestCase(AioHTTPTestCase):
    @classmethod
    def setUpClass(cls):
        if database_exists(url_psycopg):
            drop_database(url_psycopg)
        create_database(url_psycopg)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(run_init())
        loop.stop()

    async def get_application(self) -> Coroutine[Any, Any, Application]:
        application = await create_app()
        return application

    @classmethod
    def tearDownClass(cls):
        run_tear_down()

    async def client_get(self, url, params=None, headers=None):
        response = await self.client.get(url, params=params, headers=headers)
        return response

    async def client_post(self, url, data=None, headers=None):
        response = await self.client.post(url, data=json.dumps(data), headers=headers)
        return response

    async def client_delete(self, url, data=None, headers=None):
        response = await self.client.delete(url, data=json.dumps(data), headers=headers)
        return response


class BaseAuthTestCase(BaseTestCase):
    authentication_header = "Bearer "

    @classmethod
    def setUpClass(cls):
        if database_exists(url_psycopg):
            drop_database(url_psycopg)
        create_database(url_psycopg)

        loop = asyncio.new_event_loop()

        loop.run_until_complete(run_init())
        loop.run_until_complete(mock_user(1, email="admin@test.com", password="password"))
        loop.stop()

    async def login_test(self):
        response = await self.client_post("/auth/login", data={"email": "admin@test.com", "password": "password"})
        response_json = await response.json()
        self.authentication_header += response_json["result"]["access_token"]
