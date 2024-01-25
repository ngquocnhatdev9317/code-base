import asyncio

import aiohttp_autoreload
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_middlewares import cors_middleware

from database.connection import Connection, init_database
from router import add_routers
from utilities.configs import DEBUG
from utilities.constants import ENGINE_KEY
from utilities.logger import logger_info, logging
from utilities.middlewares.error_handle import error_middleware


async def create_app() -> web.Application:  # pragma: no cover
    """
    Create and configure the web application.

    Returns:
        web.Application: The configured web application.

    """

    application = web.Application(
        middlewares=[
            cors_middleware(allow_all=True, origins=["http://localhost:3000"]),
            web.normalize_path_middleware(),
            error_middleware,
        ],
        logger=logging,
    )

    add_routers(app=application)
    connect = Connection()

    if DEBUG:
        print("debug")
        loop = asyncio.get_running_loop()
        logger_info("autoreload onchange is start!")
        aiohttp_autoreload.start(loop)

    await init_database(connect.engine)
    application[ENGINE_KEY] = connect.engine
    logger_info("create connection success")

    setup_aiohttp_apispec(application, swagger_path="/docs", version="0.0.2")
    return application
