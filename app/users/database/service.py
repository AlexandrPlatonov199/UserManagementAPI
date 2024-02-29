import pathlib
from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.database.service import BaseDatabaseService
from app.common.utils.empty import Empty
from app.users.database.models import Base, User

from .settings import Settings


class Service(BaseDatabaseService):
    def get_alembic_config_path(self) -> pathlib.Path:
        return pathlib.Path(__file__).parent / "migrations"

    def get_models(self) -> list[Type[Base]]:
        return [User]

    async def get_user(
            self,
            session: AsyncSession,
            user_id: int | Type[Empty] = Empty,
            email: str | Type[Empty] = Empty,
    ) -> User | None:
        filters = []
        if user_id is not Empty:
            filters.append(User.id == user_id)
        if email is not Empty:
            filters.append(User.email == email)

        stmt = select(User).where(*filters)
        result = await session.execute(stmt)
        user = result.unique().scalar_one_or_none()

        return user

    async def update_user(
            self,
            session: AsyncSession,
            user: User,
            username: str | None | Type[Empty] = Empty,
            email: str | None | Type[Empty] = Empty
    ) -> User:
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
        user = User(
            email=email,
            username=username,
        )
        session.add(user)

        return user

    async def delete_user(
            self,
            session: AsyncSession,
            user: User,
    ) -> None:
       pass


def get_service(settings: Settings) -> Service:
    return Service(dsn=str(settings.dsn))
