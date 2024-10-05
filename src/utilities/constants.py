from aiohttp import web
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine

from authentication.schemas.authentication_schema import AuthUser

DB_KEY = web.AppKey("session_connect", AsyncEngine)
SESSION_KEY = web.AppKey("session_redis", Redis)

AUTH_KEY = web.AppKey("auth", AuthUser)

ERROR_CODE = {
    400: "ERROR_400: Invalid",
    401: "ERROR_401: Unauthorized",
    403: "ERROR_403: Forbidden",
    404: "ERROR_404: Not Found",
    405: "ERROR_405: Method Not Allowed",
    422: "ERROR_422: Validation Error",
    500: "ERROR_500: Internal Server Error",
}
