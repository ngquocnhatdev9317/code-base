from pydantic import BaseModel

from core.base.schemas.response import BaseResponseSchema


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class LoginSuccessResponseSchema(BaseResponseSchema):
    result: TokenResponseSchema
