from aiohttp import web

from authentication.controller import LoginAPIView, LogoutAPIView

authentication_view = [
    web.view("/auth/login", LoginAPIView, name="login"),
    web.view("/auth/logout", LogoutAPIView, name="logout"),
]
