from aiohttp import web
from user.controller import create_user, list_user

user_routers = [
    web.get("/user", list_user, allow_head=False),
    web.post("/user", create_user),
]
