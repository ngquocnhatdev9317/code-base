from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from core.configs import POSTGRES_DB, URL


class Connection:
    def __init__(self, engine: AsyncEngine = None) -> None:
        self.__engine = engine or create_async_engine(f"postgresql+asyncpg://{URL}/{POSTGRES_DB}")

    @property
    def engine(self) -> AsyncEngine:
        return self.__engine


def get_postgres_container(url_connection):
    engine = create_async_engine(url_connection)
    return engine
