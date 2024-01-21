from aiohttp import web
from aiohttp_apispec import docs
from user.router import user_routers


@docs(
    tags=["Heath Check"],
    summary="Check heath code",
    description="Check heath code",
    responses={
        200: {
            "description": "Success response",
        },
    },
)
async def welcome(request: web.Request):
    return web.Response(text="Welcome to home page")


def add_routers(app: web.Application):
    app.add_routes([web.get("/", welcome, name="welcome", allow_head=False)])
    app.add_routes(user_routers)
