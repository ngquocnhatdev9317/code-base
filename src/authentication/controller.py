from aiohttp import web
from aiohttp_pydantic.oas.typing import r200, r204

from authentication.schemas.request_schema import LoginRequestSchema
from authentication.schemas.response_schema import LoginSuccessResponseSchema
from authentication.service import AuthenticationService
from core.base.view import BaseView, api_docs
from user.repository import UserRepository


class LoginAPIView(BaseView):
    @property
    def repository(self):
        return UserRepository(self.request)

    @api_docs(tag="Authenticated")
    async def post(self, params: LoginRequestSchema) -> r200[LoginSuccessResponseSchema]:
        """
        API Login
        """
        service = AuthenticationService(self.request)
        token = await service.verify_login(params.email, params.password)

        return web.json_response(
            data=LoginSuccessResponseSchema(
                result={
                    "access_token": token.access_token,
                    "refresh_token": token.refresh_token,
                }
            ).model_dump(),
            status=200,
        )


class LogoutAPIView(BaseView):
    @api_docs(tag="Authenticated", authenticator=True)
    async def delete(self) -> r204:
        """
        API Logout
        """
        service = AuthenticationService(self.request)

        user = self.request["user"]

        await service.logout(access_token=user.token.access_token)

        return web.json_response(status=204)
