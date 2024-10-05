import logging

from aiohttp import web
from aiohttp_middlewares import error_middleware as generate_error_middleware
from aiohttp_middlewares.error import error_context
from pydantic_core import ValidationError

from utilities.constants import ERROR_CODE
from utilities.schemas.response_schema import ErrorResponseSchema, ErrorsResponseSchema

logger = logging.getLogger(__name__)


def get_validate_response(errors) -> web.Response:
    return web.json_response(
        ErrorsResponseSchema(
            status_code=422,
            errors_detail=[
                {
                    "error_code": ERROR_CODE[422],
                    "field": field,
                    "message": err["msg"],
                }
                for err in errors
                for field in err["loc"]
            ],
        ).model_dump(),
        status=422,
    )


async def default_error_handler(request: web.Request) -> web.Response:
    with error_context(request) as context:
        logger.error(context.message)

        if isinstance(context.err, ValidationError):
            errors = context.err.errors()
            return get_validate_response(errors)

        return web.json_response(
            ErrorResponseSchema(
                status_code=context.status,
                error_detail={
                    "error_code": ERROR_CODE[context.status],
                    "message": context.message,
                },
            ).model_dump(),
            status=context.status,
        )


error_middleware = generate_error_middleware(default_handler=default_error_handler)
