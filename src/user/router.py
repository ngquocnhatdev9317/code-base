from aiohttp import web

from user.controller import UserAPIView

user_view = [web.view("/users", UserAPIView, name="user")]
