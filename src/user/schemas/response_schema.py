from marshmallow import fields

from user.schemas.user_schema import UserSchema
from utilities.schemas.response_schema import BaseResponseSchema


class ListUserSchema(BaseResponseSchema):
    result = fields.List(
        fields.Nested(UserSchema(exclude=["is_superuser"])), required=True
    )
