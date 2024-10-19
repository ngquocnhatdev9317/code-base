import logging
from typing import Dict, List, Optional

from aiohttp.web_exceptions import HTTPBadRequest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from core.base.repository import BaseRepository
from user.model import User

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[User]):
    model = User

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieves a user from the database by their email address.

        This asynchronous function queries the database for a user with the specified email.
        It uses SQLAlchemy's select statement to perform the query and returns the result.

        Parameters:
        - email (str): The email address of the user to search for in the database.

        Returns:
        - Optional[User]: A User object if a user with the specified email is found, or None if no user is found.

        Note:
        - The database session is closed after the operation is completed.
        """
        async with self.session as session:
            result = await session.execute(select(self.model).where(self._eq("email", email)))
            await session.aclose()

            return result.scalar()

    async def get_user_by_username(self, username) -> Optional[User]:
        """
        Retrieves a user from the database by their name.

        This asynchronous function queries the database for a user with the specified name.
        It uses SQLAlchemy's select statement to perform the query and returns the result.

        Parameters:
        - name (str): The name of the user to search for in the database.

        Returns:
        - Optional[User]: A User object if a user with the specified name is found, or None if no user is found.

        Note:
        - The database session is closed after the operation is completed.
        """
        async with self.session as session:
            result = await session.execute(select(self.model).where(self._eq("username", username)))
            await session.aclose()

            return result.scalar()

    async def get_list(self, offset=0, limit=10) -> List[User]:
        """
        Retrieves a list of users from the database.

        This asynchronous function fetches a list of users from the database based on the provided offset and limit.
        It uses SQLAlchemy's select statement to query the database and returns the result as a list of User objects.

        Parameters:
        - offset (int): The starting index for fetching users. Default is 0.
        - limit (int): The maximum number of users to fetch. Default is 10.

        Returns:
        - List[User]: A list of User objects fetched from the database.

        Note:
        - The session is closed after the operation is completed.
        """
        async with self.session as session:
            result = await session.execute(select(self.model).limit(limit).offset(offset))
            await session.aclose()
            users = list(result.scalars().all())

            return users

    async def add(self, data: Dict) -> None:
        """
        Adds a new user to the database.

        This asynchronous function creates a new user in the database using the provided data.
        It handles potential integrity errors that may occur if the user already exists.

        Parameters:
        - data (Dict): A dictionary containing the user data to be added to the database.
                       The dictionary keys should correspond to the User model attributes.

        Raises:
        - HTTPBadRequest: If a user with the same unique identifier (e.g., email) already exists.

        Note:
        - The database session is closed after the operation, regardless of success or failure.
        """
        async with self.session as session:
            try:
                user = self.model(**data)
                session.add(user)
                await session.commit()
            except IntegrityError as error:
                logger.error(error)
                raise HTTPBadRequest(reason="User is already existing") from error
            finally:
                await session.aclose()
