from marshmallow import Schema, fields


class BaseResponseSchema(Schema):
    status = fields.Bool(default=True)
    status_code = fields.Int(default=200)


class SuccessResponse(BaseResponseSchema):
    message = fields.Str(required=True)


class ErrorDetailSchema(Schema):
    error_code = fields.Str(default="")
    field = fields.Str()
    message = fields.Str(required=True)


class ErrorResponseSchema(BaseResponseSchema):
    status = fields.Bool(default=False)
    error_detail = fields.Nested(ErrorDetailSchema(), required=True)
