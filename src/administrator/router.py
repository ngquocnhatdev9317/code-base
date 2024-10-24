from aiohttp import web

from administrator.controller import AdminLoginView

administrator_view = [
    web.view("/admin/login", AdminLoginView, name="administrator_login"),
]
