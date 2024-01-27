import asyncio
import json
from typing import Any, Coroutine

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import Application
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from database.base_model import BaseModel
from main import create_app
from utilities.configs import SCHEMA, URL

url_asyncpg = f"postgresql+asyncpg://{URL}/{SCHEMA}"
url_psycopg = url_asyncpg.replace("asyncpg", "psycopg2")


def get_postgres_container():
    engine = create_async_engine(url_asyncpg)
    return engine


async def run_init():
    engine = get_postgres_container()

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

    async def client_get(self, url, params=None):
        request = self.client.get(url, params=params)
        return await request

    async def client_post(self, url, data=None):
        request = self.client.post(url, data=json.dumps(data))
        return await request
