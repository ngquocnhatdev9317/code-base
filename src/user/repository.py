from typing import Dict, List

from sqlalchemy import select

from database.base_repository import BaseRepository
from user.model import User


class UserRepository(BaseRepository[User]):
    model = User

    async def get_user_by_email(self, email: str) -> User | None:
        async with self.session as session:
            result = await session.execute(select(self.model).where(self._eq("email", email)))
            await session.aclose()

            return result.scalar()

    async def get_list(self, offset=0, limit=10) -> List[User]:
        async with self.session as session:
            result = await session.execute(select(self.model).limit(limit).offset(offset))
            await session.aclose()
            users = list(result.scalars().all())

            return users

    async def add(self, data: Dict):
        """
                Adds a new user to the database.

                This asynchronous function takes user data, hashes the password,
                creates a new User object, and adds it to the database.

                Parameters:
                    data (dict): A dictionary containing user information.
                                    It should include at least a 'password' key.

                Returns:
        `            None:

                Note:
                - The function modifies the 'password' in the input data by hashing it.
                - The session is closed after the operation is completed.
        """
        async with self.session as session:
            user = self.model(**data)
            session.add(user)
            await session.commit()

            await session.aclose()
