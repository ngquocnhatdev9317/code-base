import datetime
import logging

import jwt
from passlib.hash import pbkdf2_sha256
from redis.asyncio import Redis

from authentication.schemas.authentication_schema import AuthUser, Token
from database.base_service import BaseService
from user.repository import UserRepository
from utilities.configs import ACCESS_EXPIRE, REFRESH_EXPIRE, SECRET_CODE
from utilities.constants import SESSION_KEY

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

        return None

    async def logout(self, access_token):
        await self.redis.delete(access_token)

    async def get_token(self, email: str) -> Token:
        access_token_exp = datetime.datetime.now() + datetime.timedelta(seconds=ACCESS_EXPIRE)
        refresh_token_exp = datetime.datetime.now() + datetime.timedelta(seconds=REFRESH_EXPIRE)
        access_token = jwt.encode(
            {"email": email, "exp": access_token_exp},
            SECRET_CODE,
        )
        refresh_token = jwt.encode(
            {"email": email, "exp": refresh_token_exp},
            SECRET_CODE,
        )
        await self.redis.setex(access_token, ACCESS_EXPIRE, 1)
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def verify_access(self, access_token):
        result = await self.redis.getex(access_token)
        if not result:
            return None
        payload = jwt.decode(access_token, SECRET_CODE, algorithms=["HS256"])
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
