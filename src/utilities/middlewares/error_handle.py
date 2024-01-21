from aiohttp import web
from aiohttp_middlewares import error_middleware as generate_error_middleware
from aiohttp_middlewares.error import error_context
from utilities.logger import logger_error
from utilities.schemas.response_schema import ErrorResponseSchema


async def default_error_handler(request: web.Request) -> web.Response:
    with error_context(request) as context:
        logger_error(context.message)
        return web.json_response(
            ErrorResponseSchema().dump(
                {
                    "status_code": context.status,
                    "error_detail": {
                        "error_code": "",
                        "message": context.message,
                    },
                }
            ),
            status=context.status,
        )


error_middleware = generate_error_middleware(default_handler=default_error_handler)
