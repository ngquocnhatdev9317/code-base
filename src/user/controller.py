from aiohttp import web
from aiohttp_pydantic.oas.typing import r200, r201

from user.schemas.request_schema import CreateUserSchema
from user.schemas.response_schema import ListUserResponseSchema
from user.service import UserService
from utilities.base_view import BaseView
from utilities.schemas.request_schema import PaginationRequest
from utilities.schemas.response_schema import SuccessResponse


class UserAPIView(BaseView):
    async def get(self, params: PaginationRequest) -> r200[ListUserResponseSchema]:
        """
        Get user list

        Tags: User
        """
        service = UserService(self.request)
        data = await service.get_list(params)

        return web.json_response(
            data=ListUserResponseSchema(result=data).model_dump(),
            status=200,
        )

    async def post(self, user_params: CreateUserSchema) -> r201[SuccessResponse]:
        """
        Create user

        Tags: User
        """
        service = UserService(self.request)
        await service.add_user(user_params.model_dump())

        return web.json_response(
            data=SuccessResponse(message="Create user success!").model_dump(),
            status=201,
        )
