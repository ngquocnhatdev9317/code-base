import logging

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp_middlewares import cors_middleware
from aiohttp_pydantic import oas
from redis.asyncio import Redis

from database.connection import Connection
from router import add_routers
from utilities.configs import REDIS_HOST, REDIS_PORT
from utilities.constants import DB_KEY, SESSION_KEY
from utilities.functions import get_path
from utilities.middlewares.error_handle import error_middleware
from utilities.middlewares.logger_handle import logger_middleware

logger = logging.getLogger(__name__)


async def startup_connection(app: web.Application):
    redis = Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0,
    )

    app[DB_KEY] = Connection().engine
    app[SESSION_KEY] = redis
    logger.info("create connection success")
    yield
    logger.info("shutdown server success")
    await app[DB_KEY].dispose()
    await app[SESSION_KEY].close()


async def create_app() -> web.Application:
    """
    Create and configure the web application.

    Returns:
        web.Application: The configured web application.

    """

    application = web.Application(
        middlewares=[
            cors_middleware(allow_all=True, origins=["http://localhost:3000"]),
            web.normalize_path_middleware(),
            logger_middleware,
            error_middleware,
        ],
        logger=logging,
    )
    application.add_routes([web.static("/s", path=get_path("public"))])

    add_routers(app=application)

    application.cleanup_ctx.append(startup_connection)

    oas.setup(
        application,
        url_prefix="/docs",
        title_spec="Codebase application",
        version_spec="0.0.1",
        security={"bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}},
    )
    aiohttp_jinja2.setup(
        application,
        loader=jinja2.FileSystemLoader(get_path("templates")),
    )

    return application
