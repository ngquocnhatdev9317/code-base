from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession

from utilities.constants import ENGINE_KEY


class BaseRepository:
    def __init__(self, request: web.Request) -> None:
        self.__engine = request.app[ENGINE_KEY]

    @property
    def session(self):
        return AsyncSession(self.__engine, expire_on_commit=False)
