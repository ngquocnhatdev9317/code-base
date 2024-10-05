from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

constraint_naming_conventions = {
    "ix": "IX_%(column_0_N_label)s",
    "uq": "UQ_%(table_name)s_%(column_0_N_name)s",
    "ck": "CK_%(table_name)s_%(constraint_name)s",
    "fk": "FK_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "PK_%(table_name)s",
}

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    created_at = sa.Column(sa.DateTime, default=datetime.now())
    updated_at = sa.Column(sa.DateTime, default=datetime.now(), onupdate=datetime.now())

    metadata = sa.MetaData(naming_convention=constraint_naming_conventions)

    def __repr__(self):
        return f"<{self.__class__.__name__} (id={self.id})>"
