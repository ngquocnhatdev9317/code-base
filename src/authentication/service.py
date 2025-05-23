import datetime
import logging

import jwt
from aiohttp.web_exceptions import HTTPUnauthorized
from passlib.hash import pbkdf2_sha256
from redis.asyncio import Redis

from authentication.schemas.authentication_schema import AuthUser, Token
from core.base.service import BaseService
from core.constants import SESSION_KEY
from core.settings import settings
from user.repository import UserRepository

logger = logging.getLogger(__name__)


class AuthenticationService(BaseService[UserRepository]):
    repository_class = UserRepository

    @property
    def redis(self) -> Redis:
        return self._request.app[SESSION_KEY]

    async def verify_login(self, email: str, password: str) -> Token | None:
        user = await self.repository.get_user_by_email(email)

        if user and pbkdf2_sha256.verify(password, user.password):
            token = await self.get_token(email)

            return token

        raise HTTPUnauthorized(reason="The user name or password are incorrect.")

    async def logout(self, access_token):
        await self.redis.delete(access_token)

    async def get_token(self, email: str) -> Token:
        access_token_exp = datetime.datetime.now() + datetime.timedelta(seconds=settings.access_expire)
        refresh_token_exp = datetime.datetime.now() + datetime.timedelta(seconds=settings.refresh_expire)
        access_token = jwt.encode(
            {"email": email, "exp": access_token_exp},
            settings.secret_code,
        )
        refresh_token = jwt.encode(
            {"email": email, "exp": refresh_token_exp},
            settings.secret_code,
        )
        await self.redis.setex(access_token, settings.access_expire, 1)
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def verify_access(self, access_token):
        result = await self.redis.getex(access_token)
        if not result:
            return None

        try:
            payload = jwt.decode(access_token, settings.secret_code, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPUnauthorized(reason="Access token expired")
        except jwt.InvalidTokenError:
            raise HTTPUnauthorized(reason="Invalid access token")

        email = payload.get("email")

        user = await self.repository.get_user_by_email(email)

        if not user:
            return None

        return AuthUser(
            id=user.id,
            email=user.email,
            token={
                "access_token": access_token,
            },
        )
