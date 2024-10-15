from typing import List

from aiohttp.web_exceptions import HTTPBadRequest
from passlib.hash import pbkdf2_sha256

from core.base.schemas.request import PaginationRequest
from core.base.service import BaseService
from user.model import User
from user.repository import UserRepository
from user.schemas.user_schema import UserSchema


class UserService(BaseService[UserRepository]):
    repository_class = UserRepository

    async def get_list(self, params: PaginationRequest) -> List[UserSchema]:
        offset = (params.page - 1) * params.page_size
        limit = params.page_size

        users: List[User] = await self.repository.get_list(offset=offset, limit=limit)

        return [UserSchema.model_validate(user).model_dump() for user in users]

    async def add_user(self, data: dict):
        user = await self.repository.get_user_by_email(data.get("email"))
        if user:
            raise HTTPBadRequest(reason="Email is already in use")

        user = await self.repository.get_user_by_username(data.get("username"))
        if user:
            raise HTTPBadRequest(reason="Username is already in use")

        data["password"] = pbkdf2_sha256.hash(data.get("password"))

        await self.repository.add(data)
