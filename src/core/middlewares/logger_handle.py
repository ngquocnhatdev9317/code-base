import logging

from aiohttp import web

logger = logging.getLogger(__name__)


@web.middleware
async def logger_middleware(request: web.Request, handler):
    logger.info("%s %s Location: %s", request.method.upper(), request.path, request.remote)
    response: web.Response = await handler(request)
    logger.info("%s %s", response.status, response.reason.upper())

    return response
