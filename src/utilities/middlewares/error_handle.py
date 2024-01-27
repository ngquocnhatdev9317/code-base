import ast

from aiohttp import web
from aiohttp_middlewares import error_middleware as generate_error_middleware
from aiohttp_middlewares.error import error_context
from marshmallow.exceptions import ValidationError

from utilities.logger import logger_error
from utilities.schemas.response_schema import ErrorResponseSchema, ErrorsResponseSchema


async def default_error_handler(request: web.Request) -> web.Response:
    with error_context(request) as context:
        if isinstance(context.err, ValidationError):
            errors = ast.literal_eval(context.message)
            logger_error(errors)
            return web.json_response(
                ErrorsResponseSchema().dump(
                    {
                        "status_code": 400,
                        "errors_detail": [
                            {
                                "error_code": "VALIDATION_ERROR",
                                "field": k,
                                "message": v[0],
                            }
                            for k, v in errors.items()
                        ],
                    }
                ),
                status=400,
            )

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
