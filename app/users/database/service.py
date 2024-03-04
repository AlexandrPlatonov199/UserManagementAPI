import pathlib
from typing import Type

from pydantic import EmailStr
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.database.service import BaseDatabaseService
from app.common.utils.empty import Empty
from app.users.database.models import Base, User

from .settings import Settings


class Service(BaseDatabaseService):
    """
    The Service class provides methods to interact with the database for user-related operations.

    Methods:
        get_alembic_config_path: Return the path to the Alembic configuration file.
        get_models: Return a list of SQLAlchemy models used by the service.
        get_user: Get a user object from the database by ID or email.
        update_user: Update a user's username or email.
        create_user: Create a new user object in the database.
        delete_user: Delete a user object from the database.
    """
    def get_alembic_config_path(self) -> pathlib.Path:
        """
        Return the path to the Alembic configuration file.

        Returns:
            A pathlib.Path object representing the path to the configuration file.
        """
        return pathlib.Path(__file__).parent / "migrations"

    def get_models(self) -> list[Type[Base]]:
        """
        Return a list of SQLAlchemy models used by the service.

        Returns:
            A list of SQLAlchemy model classes.
        """
        return [User]

    async def get_user(
            self,
            session: AsyncSession,
            user_id: int | Type[Empty] = Empty,
            email: str | Type[Empty] = Empty,
    ) -> User | None:
        """
        Get a user object from the database by ID or email.

        Args:
            session: The SQLAlchemy session object.
            user_id: The ID of the user to retrieve.
            email: The email address of the user to retrieve.

        Returns:
            The user object with the specified ID or email, or None if the user is not found.
        """
        filters = []
        if user_id is not Empty:
            filters.append(User.id == user_id)
        if email is not Empty:
            filters.append(User.email == email)

        stmt = select(User).where(*filters)
        result = await session.execute(stmt)
        user = result.unique().scalar_one_or_none()

        return user

    async def get_users(
        self,
        session: AsyncSession,
        page: int = 1,
        per_page: int = 10,
    ) -> list[User]:
        """
        Get a list of users with pagination.

         Args:
             session: The SQLAlchemy session object.
             page: The page number to retrieve (default is 1).
            per_page: The number of users per page (default is 10).

         Returns:
             A list of User objects.
         """
        query = select(User).order_by(User.registration_date.desc())

        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)

        result = await session.execute(query)

        return list(result.unique().scalars().all())

    async def get_user_count(
            self,
            session: AsyncSession,
    ) -> int:
        """
        Get the total number of users.

        Args:
            session: The SQLAlchemy session object.

        Returns:
            The total number of users.
        """
        query = select(func.count(User.id)) # pylint: disable=not-callable

        result = await session.scalar(query)

        return result

    async def get_users_count_last_seven_days(
            self,
            session: AsyncSession,
            seven_days_ago,
    ) -> int:
        """
        Get the number of users who registered in the last seven days.

        Args:
            session: The SQLAlchemy session object.
            seven_days_ago: A datetime object representing the date and time seven days ago.

        Returns:
            The number of users who registered in the last seven days.
        """
        stmt = select(func.count(User.id)).where(User.registration_date >= seven_days_ago)
        result = await session.execute(stmt)
        user_count = result.scalar_one()

        return user_count

    async def get_users_top_five_longest(
            self,
            session: AsyncSession,
            page: int = 1,
            per_page: int = 5,
    ) -> list[User]:
        """
        Get a paginated list of the top five users with the longest usernames.

        Args:
            session: The SQLAlchemy session object.
            page: The page number to retrieve. Defaults to 1.
            per_page: The number of users to retrieve per page. Defaults to 5.

        Returns:
            A list of `User` objects representing the top five users with the longest usernames,
            ordered by username length in descending order.
        """
        query = (
            select(User)
            .order_by(func.length(User.username).desc())
        )
        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)
        result = await session.execute(query)

        return list(result.unique().scalars().all())


    async def get_email_domain_ratio(
            self,
            session: AsyncSession,
            domain: str,
    ) -> float:
        """
        Get the ratio of users with email addresses from a specific domain.

        Args:
            session: The SQLAlchemy session object.
            domain: The domain to filter email addresses by.

        Returns:
            A float representing the ratio of users with email addresses from the specified domain,
            rounded to two decimal places. If no users have email addresses from the specified domain,
            returns 0.0.
        """
        subquery = (
            select(func.count(User.id))
            .where(User.email.like(f"%{domain}"))
        )
        total_users_subquery = select(func.count(User.id))
        query = (
            select(func.round((subquery.subquery().c.count / total_users_subquery.subquery().c.count) * 100, 2))
        )
        result = await session.execute(query)
        ratio = result.scalar_one_or_none()

        return ratio if ratio else 0.0

    async def update_user(
            self,
            session: AsyncSession,
            user: User,
            username: str | None | Type[Empty] = Empty,
            email: str | None | Type[Empty] = Empty
    ) -> User:
        """
        Update a user's username or email.

        Args:
            session: The SQLAlchemy session object.
            user: The user object to update.
            username: The new username for the user.
            email: The new email address for the user.

        Returns:
            The updated user object.
        """
        if username is not Empty:
            user.username = username
        if email is not Empty:
            user.email = email
        session.add(user)

        return user

    async def create_user(
            self,
            session: AsyncSession,
            email: str,
            username: str
    ) -> User:
        """
        Create a new user object in the database.

        Args:
            session: The SQLAlchemy session object.
            email: The email address of the new user.
            username: The username of the new user.

        Returns:
            The newly created user object.
        """
        user = User(email=email,
                    username=username)
        session.add(user)

        return user

    async def delete_user(
            self,
            session: AsyncSession,
            user: User,
    ) -> User:
        """
        Delete a user object from the database.

        Args:
            session: The SQLAlchemy session object.
            user: The user object to delete.

        Returns:
            The deleted user object.
        """

        await session.delete(user)
        await session.commit()

        return user


def get_service(settings: Settings) -> Service:
    """
    Create and return a new instance of the Service class.

    Args:
        settings: The application settings object.

    Returns:
        A new instance of the Service class.
    """
    return Service(dsn=str(settings.dsn))
