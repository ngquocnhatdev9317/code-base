from typing import List

from user.schemas.user_schema import UserSchema
from utilities.schemas.response_schema import BaseResponseSchema


class ListUserResponseSchema(BaseResponseSchema):
    result: List[UserSchema]
