from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from database.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    @declared_attr.directive
    def __table_args__(self):
        return (UniqueConstraint("name", "email"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<User (id={self.id})>"
