from aiohttp import web
from database.base_repository import BaseRepository
from sqlalchemy import select
from user.model import User
from user.schemas.user_schema import UserSchema


class UserRepository(BaseRepository):
    def __init__(self, request: web.Request) -> None:
        super().__init__(request)

    async def get_list(self):
        async with self.session as session:
            result = await session.execute(select(User))
            await session.aclose()
            users = result.scalars().all()
            return UserSchema().dump(users, many=True)

    async def add_user(self, data):
        async with self.session as session:
            user = UserSchema().load(data, session=session)
            session.add(user)
            await session.commit()

            await session.aclose()
