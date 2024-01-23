from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncEngine

ENGINE_KEY = web.AppKey("engine", AsyncEngine)
