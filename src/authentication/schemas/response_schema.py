from pydantic import BaseModel

from utilities.schemas.response_schema import BaseResponseSchema


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class LoginSuccessResponseSchema(BaseResponseSchema):
    result: TokenResponseSchema
