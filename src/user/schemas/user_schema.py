from marshmallow_sqlalchemy import auto_field

from database.base_schema import BaseSchema
from user.model import User


class UserSchema(BaseSchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field()
    name = auto_field()
    email = auto_field()
    is_superuser = auto_field()
