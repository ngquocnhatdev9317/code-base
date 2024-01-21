from database.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return "<User (id={self.id})>".format(self=self)
