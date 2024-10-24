import json
from typing import Any, Coroutine

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import Application
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from core.base.model import BaseModel
from core.configs import POSTGRES_DB, URL
from main import create_app
from tests.mockup import mock_user

url_psycopg = f"postgresql+psycopg2://{URL}/{POSTGRES_DB}"


def run_init():
    engine = create_engine(url_psycopg)

    with engine.begin() as conn:
        BaseModel.metadata.create_all(conn)
    engine.dispose()


def run_tear_down():
    drop_database(url_psycopg)


class BaseTestCase(AioHTTPTestCase):
    @classmethod
    def setUpClass(cls):
        if database_exists(url_psycopg):
            drop_database(url_psycopg)
        create_database(url_psycopg)

        run_init()

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

        run_init()
        mock_user(1, email="admin@test.com", password="password")

    async def login_test(self):
        response = await self.client_post("/auth/login", data={"email": "admin@test.com", "password": "password"})
        response_json = await response.json()
        self.authentication_header += response_json["result"]["access_token"]
