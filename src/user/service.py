from typing import List

from passlib.hash import pbkdf2_sha256

from database.base_service import BaseService
from user.model import User
from user.repository import UserRepository
from user.schemas.user_schema import UserSchema
from utilities.schemas.request_schema import PaginationRequest


class UserService(BaseService[UserRepository]):
    repository_class = UserRepository

    async def get_list(self, params: PaginationRequest) -> List[UserSchema]:
        offset = (params.page - 1) * params.page_size
        limit = params.page_size

        users: List[User] = await self.repository.get_list(offset=offset, limit=limit)

        return [UserSchema.model_validate(user).model_dump() for user in users]

    async def add_user(self, data: dict):
        data["password"] = pbkdf2_sha256.hash(data.get("password"))

        await self.repository.add(data)
