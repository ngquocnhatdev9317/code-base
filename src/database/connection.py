from sqlalchemy.ext.asyncio import create_async_engine

from utilities.configs import URL


class Connection:
    def __init__(self) -> None:
        self.__engine = create_async_engine(f"postgresql+asyncpg://{URL}")

    @property
    def engine(self):
        return self.__engine
