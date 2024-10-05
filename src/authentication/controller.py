from aiohttp import web
from aiohttp_pydantic.oas.typing import r200, r204

from authentication.schemas.request_schema import LoginRequestSchema
from authentication.schemas.response_schema import LoginSuccessResponseSchema
from authentication.service import AuthenticationService
from user.repository import UserRepository
from utilities.authentical_policy import authentication_class_wrapper
from utilities.base_view import BaseView
from utilities.constants import AUTH_KEY


class LoginAPIView(BaseView):
    @property
    def repository(self):
        return UserRepository(self.request)

    async def post(self, params: LoginRequestSchema) -> r200[LoginSuccessResponseSchema]:
        """
        Login

        Tags: Authenticated
        """
        service = AuthenticationService(self.request)
        token = await service.verify_login(params.email, params.password)

        if token:
            return web.json_response(
                data=LoginSuccessResponseSchema(
                    result={
                        "access_token": token.access_token,
                        "refresh_token": token.refresh_token,
                    }
                ).model_dump(),
                status=200,
            )

        return web.json_response(status=400)


@authentication_class_wrapper
class LogoutAPIView(BaseView):
    async def delete(self) -> r204:
        """
        Logout

        Tags: Authenticated
        """
        service = AuthenticationService(self.request)

        user = self.request.app[AUTH_KEY]

        await service.logout(access_token=user.token.access_token)

        return web.json_response(status=204)
