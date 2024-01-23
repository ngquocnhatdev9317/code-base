import logging
from typing import Any, Coroutine

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp.web import Application

from database.connection import Connection
from router import add_routers
from utilities.constants import ENGINE_KEY
from utilities.middlewares.error_handle import error_middleware


class BaseTestCase(AioHTTPTestCase):
    async def get_application(self) -> Coroutine[Any, Any, Application]:
        application = Application(
            middlewares=[
                error_middleware,
            ],
            logger=logging,
        )

        add_routers(app=application)
        connect = Connection()

        application[ENGINE_KEY] = connect.engine
        return application
