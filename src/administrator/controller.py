import aiohttp_jinja2

from authentication.schemas.request_schema import LoginRequestSchema
from core.base.view import BaseView


class AdminLoginView(BaseView):
    @aiohttp_jinja2.template("pages/admin/login.html.j2")
    async def get(self):
        return {"email": "", "password": ""}

    async def post(self, params: LoginRequestSchema):
        print("oke", params)
        return {"email": params.email, "password": params.password}
