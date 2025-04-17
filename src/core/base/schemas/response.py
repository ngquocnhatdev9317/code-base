from typing import List, Optional, Union

from pydantic import BaseModel


class BaseResponseSchema(BaseModel):
    status: bool = True
    status_code: int = 200


class SuccessResponse(BaseResponseSchema):
    message: str


class ErrorFieldDetailSchema(BaseModel):
    error_code: Optional[str] = None
    field: str
    message: str


class ErrorDetailSchema(BaseModel):
    error_code: Optional[str] = None
    message: str


class ErrorResponseSchema(BaseResponseSchema):
    status: bool = False
    error_detail: ErrorDetailSchema


class ErrorsResponseSchema(BaseResponseSchema):
    status: bool = False
    errors_detail: Union[List[Union[ErrorFieldDetailSchema, ErrorDetailSchema]], List]
