from typing import Dict, Generic, List, TypeVar

from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.constants import DB_KEY

T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: type[T]

    def __init__(self, request: web.Request) -> None:
        self.__engine = request.app[DB_KEY]

    @property
    def session(self):
        return AsyncSession(self.__engine, expire_on_commit=False)

    async def get_list(self, offset: int = 0, limit: int = 10) -> List[T]:
        pass

    async def get_by_id(self, id: int) -> T:
        pass

    async def add(self, data: Dict) -> None:
        pass

    def _eq(self, key, value):
        return self.model.__table__.c[key] == value

    def _gt(self, key, value):
        return self.model.__table__.c[key] < value

    def _gte(self, key, value):
        return self.model.__table__.c[key] <= value

    def _lt(self, key, value):
        return self.model.__table__.c[key] > value

    def _lte(self, key, value):
        return self.model.__table__.c[key] >= value

    def _like(self, key, value):
        return self.model.__table__.c[key].like(value)
