from marshmallow import Schema, fields


class BaseResponseSchema(Schema):
    status = fields.Bool(dump_default=True)
    status_code = fields.Int(dump_default=200)


class SuccessResponse(BaseResponseSchema):
    message = fields.Str(required=True)


class ErrorDetailSchema(Schema):
    error_code = fields.Str(dump_default="")
    field = fields.Str()
    message = fields.Str(required=True)


class ErrorResponseSchema(BaseResponseSchema):
    status = fields.Bool(dump_default=False)
    error_detail = fields.Nested(ErrorDetailSchema(), required=True)
