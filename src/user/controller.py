from aiohttp import web
from aiohttp_pydantic.oas.typing import r200, r201

from core.base.schemas.request import PaginationRequest
from core.base.schemas.response import SuccessResponse
from core.base.view import BaseView, api_docs
from user.schemas.request_schema import CreateUserSchema
from user.schemas.response_schema import ListUserResponseSchema
from user.service import UserService


class UserAPIView(BaseView):
    @api_docs(tag="User")
    async def get(self, params: PaginationRequest) -> r200[ListUserResponseSchema]:
        """
        Get user list
        """

        service = UserService(self.request)
        data = await service.get_list(params)

        return web.json_response(
            data=ListUserResponseSchema(result=data).model_dump(),
            status=200,
        )

    @api_docs(tag="User", response={201: "Created user successful."})
    async def post(self, user_params: CreateUserSchema) -> r201[SuccessResponse]:
        """
        Create user
        """

        service = UserService(self.request)
        await service.add_user(user_params.model_dump())

        return web.json_response(
            data=SuccessResponse(message="Create user success!").model_dump(),
            status=201,
        )
