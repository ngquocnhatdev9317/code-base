from aiohttp import web
from aiohttp_apispec import docs, json_schema

from user.repository import UserRepository
from user.schemas.request_schema import CreateUserSchema
from user.schemas.response_schema import ListUserSchema
from utilities.schemas.response_schema import ErrorResponseSchema, SuccessResponse


@docs(
    tags=["User"],
    summary="Get list user",
    description="Get list user",
    responses={
        200: {
            "schema": ListUserSchema,
            "description": "Success response",
        },
        400: {
            "schema": ErrorResponseSchema,
            "description": "Error response",
        },
        500: {
            "schema": ErrorResponseSchema,
            "description": "Error response",
        },
    },
)
async def list_user(request: web.Request):
    repo = UserRepository(request)
    data = await repo.get_list()
    return web.json_response(
        data=ListUserSchema().dump({"result": data}),
        status=200,
    )


@docs(
    tags=["User"],
    summary="Add user",
    description="Add user",
    responses={
        201: {
            "schema": SuccessResponse,
            "description": "Success response",
        },
        400: {
            "schema": ErrorResponseSchema,
            "description": "Error response",
        },
        500: {
            "schema": ErrorResponseSchema,
            "description": "Error response",
        },
    },
)
@json_schema(CreateUserSchema())
async def create_user(request: web.Request):
    user_data = await request.json()
    repo = UserRepository(request)
    await repo.add_user(user_data)

    return web.json_response(
        data=SuccessResponse().dump({"message": "Create user success!"}), status=201
    )
