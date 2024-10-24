# pylint: disable=unused-argument
import aiohttp_jinja2
from aiohttp import web

from administrator.router import administrator_view
from authentication.router import authentication_view
from user.router import user_view


@aiohttp_jinja2.template("pages/index.html.j2")
async def welcome(request: web.Request):
    return {"version": "is_data"}


def add_routers(app: web.Application):
    app.add_routes([web.get("/", welcome, name="welcome", allow_head=False)])
    app.add_routes(user_view)
    app.add_routes(authentication_view)
    app.add_routes(administrator_view)
