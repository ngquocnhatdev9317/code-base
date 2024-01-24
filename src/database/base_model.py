from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

constraint_naming_conventions = {
    "ix": "IX_%(column_0_N_label)s",
    "uq": "UQ_%(table_name)s_%(column_0_N_name)s",
    "ck": "CK_%(table_name)s_%(constraint_name)s",
    "fk": "FK_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "PK_%(table_name)s",
}


class BaseModel(DeclarativeBase):
    metadata = MetaData(naming_convention=constraint_naming_conventions)
