from marshmallow import Schema, fields


class CreateUserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
