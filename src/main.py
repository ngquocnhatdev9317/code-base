import asyncio

import aiohttp_autoreload
from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_middlewares import cors_middleware
from sqlalchemy.ext.asyncio import AsyncEngine

from database.base_model import BaseModel
from database.connection import Connection
from router import add_routers
from utilities.constants import ENGINE_KEY
from utilities.logger import logger_info, logging
from utilities.middlewares.error_handle import error_middleware


async def init_database(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

        logger_info("initialized database")


def create_app() -> web.Application:
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

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_database(connect.engine))
    aiohttp_autoreload.start(loop)

    application[ENGINE_KEY] = connect.engine
    logger_info("create connection success")

    setup_aiohttp_apispec(application, swagger_path="/docs", version="0.0.2")
    return application


app = create_app()

# async def start_server(host="0.0.0.0", port=8080):
#     runner = await create_runner()
#     await runner.setup()
#     site = web.TCPSite(runner, host, port)
#     logger_info("server starter")
#     await site.start()


# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     aiohttp_autoreload.start(loop)
#     loop.run_until_complete(start_server())
#     loop.run_forever()
