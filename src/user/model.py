import sqlalchemy as sa
from sqlalchemy.orm import declared_attr

from database.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name = sa.Column(sa.String(30), unique=True)
    email = sa.Column(sa.String(50), unique=True)
    password = sa.Column(sa.String(200))
    is_superuser = sa.Column(sa.Boolean, default=False)

    @declared_attr.directive
    def __table_args__(self):
        return (sa.UniqueConstraint("name", "email"),)
