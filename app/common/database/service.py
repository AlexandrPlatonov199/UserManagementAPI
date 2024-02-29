import pathlib
from contextlib import asynccontextmanager
from typing import Type

from alembic import command as alembic_command
from alembic.config import Config as AlembicConfig
from facet import ServiceMixin
from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class BaseDatabaseService(ServiceMixin):
    """
    Base class for defining database services.

    Attributes:
        _dsn (str): The URL of the database connection string.
        _engine (Engine): The SQLAlchemy engine used to connect to the database.
        _sessionmaker (SessionLocal): A factory used to create database sessions.

    Methods:
         get_alembic_config_path: Returns the path to the Alembic configuration file.
        get_alembic_config: Returns an Alembic configuration object.
        get_models: Returns a list of SQLAlchemy models.
        transaction: Returns an asynchronous context manager for a database transaction.
        migrate: Applies all pending database migrations.
        rollback: Rolls back the database to a specified revision.
        show_migrations: Shows a list of database migrations.
        create_migration: Creates a new database migration with a specified message.
        start: Starts the database service.
        stop: Stops the database service.
    """
    def __init__(self, dsn: str):
        """
        Initializes the database service.

        Args:
            dsn (str): The URL of the database connection string.
        """
        self._dsn = dsn
        self._engine = create_async_engine(self._dsn, pool_recycle=60)
        self._sessionmaker = async_sessionmaker(self._engine, expire_on_commit=False)

    def get_alembic_config_path(self) -> pathlib.Path:
        """
        Returns the path to the Alembic configuration file.

        Returns:
            pathlib.Path: The path to the Alembic configuration file.
        """
        raise NotImplementedError

    def get_alembic_config(self) -> AlembicConfig:
        """
        Returns an Alembic configuration object.

        Returns:
            alembic_config.Config: An Alembic configuration object.
        """
        migrations_path = self.get_alembic_config_path()

        config = AlembicConfig()
        config.set_main_option("script_location", str(migrations_path))
        config.set_main_option("sqlalchemy.url", self._dsn.replace("%", "%%"))

        return config

    def get_models(self) -> list[Type[DeclarativeBase]]:
        """
        Returns a list of SQLAlchemy models.

        Returns:
            List[Type[DeclarativeBase]]: A list of SQLAlchemy models.
        """
        raise NotImplementedError(
            "For working with fixtures you need override `get_models_mapping` method",
        )

    @asynccontextmanager
    async def transaction(self):
        """
        Returns an asynchronous context manager for a database transaction.

        Yields:
            AsyncContextManager[Any]: An asynchronous context manager for a database transaction.
        """
        async with self._sessionmaker() as session:
            async with session.begin():
                yield session

    def migrate(self):
        """
        Applies all pending database migrations.
        """
        alembic_command.upgrade(self.get_alembic_config(), "head")

    def rollback(self, revision: str | None = None):
        """
        Rolls back the database to a specified revision.

        Args:
            revision (str, optional): The revision to roll back to. Defaults to "-1".
        """
        revision = revision or "-1"

        alembic_command.downgrade(self.get_alembic_config(), revision)

    def show_migrations(self):
        """
        Shows a list of database migrations.
        """
        alembic_command.history(self.get_alembic_config())

    def create_migration(self, message: str | None = None):
        """
        Creates a new database migration with a specified message.

        Args:
            message (str, optional): The message for the migration. Defaults to None.
        """
        alembic_command.revision(
            self.get_alembic_config(), message=message, autogenerate=True,
        )

    async def start(self):
        """
        Starts the database service.
        """
        logger.info("Start Database service")

    async def stop(self):
        """
        Stops the database service.
        """
        logger.info("Stop Database service")
