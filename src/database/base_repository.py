from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, request: web.Request) -> None:
        self.__engine = request.app["engine"]

    @property
    def session(self):
        return AsyncSession(self.__engine, expire_on_commit=False)
