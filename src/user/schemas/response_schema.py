from typing import List

from core.base.schemas.response import BaseResponseSchema
from user.schemas.user_schema import UserSchema


class ListUserResponseSchema(BaseResponseSchema):
    result: List[UserSchema]
