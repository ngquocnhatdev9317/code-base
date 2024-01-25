from typing import Any, Coroutine

import pytest
from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import Application, normalize_path_middleware
from aiohttp_middlewares import cors_middleware
from sqlalchemy.ext.asyncio import create_async_engine

from database.connection import Connection, init_database
from router import add_routers
from utilities.constants import ENGINE_KEY
from utilities.middlewares.error_handle import error_middleware


def get_postgres_container():
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:password@localhost:5432/dummy"
    )
    print("mock engine")
    return engine


@pytest.fixture(scope="module")
def engine_mock():
    return get_postgres_container()


class BaseTestCase(AioHTTPTestCase):
    async def get_application(self) -> Coroutine[Any, Any, Application]:
        application = Application(
            middlewares=[
                cors_middleware(allow_all=True, origins=["http://localhost:3000"]),
                normalize_path_middleware(),
                error_middleware,
            ],
        )

        add_routers(app=application)
        connect = Connection(engine=get_postgres_container())

        await init_database(connect.engine)
        application[ENGINE_KEY] = connect.engine
        return application
