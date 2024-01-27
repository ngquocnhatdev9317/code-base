from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from database.base_model import BaseModel
from utilities.configs import SCHEMA, URL
from utilities.logger import logger_info


class Connection:
    def __init__(self, engine: AsyncEngine = None) -> None:
        self.__engine = engine or create_async_engine(
            f"postgresql+asyncpg://{URL}/{SCHEMA}"
        )

    @property
    def engine(self):
        return self.__engine

    async def init_database(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)

            logger_info("initialized database")
