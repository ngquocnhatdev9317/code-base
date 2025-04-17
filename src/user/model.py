import sqlalchemy as sa
from sqlalchemy.orm import declared_attr

from core.base.model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = sa.Column(sa.String(30), unique=True)
    first_name = sa.Column(sa.String())
    last_name = sa.Column(sa.String())
    full_name = sa.Column(sa.String())
    email = sa.Column(sa.String(50), unique=True)
    password = sa.Column(sa.String(200))
    is_superuser = sa.Column(sa.Boolean, default=False)

    @declared_attr.directive
    def __table_args__(self):
        return (sa.UniqueConstraint("username", "email"),)
