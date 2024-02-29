from pydantic import AnyUrl

from app.common.database.settings import BaseDatabaseSettings


class Settings(BaseDatabaseSettings):
    """Settings class for the database.

    This class is used to represent the settings required by the database, including the settings inherited from the
    `BaseDatabaseSettings` class.

    Attributes:
        dsn (AnyUrl): The data source name for the database. This should be a URL-like string that specifies the type
                      of database, the host, the port, and the name of the database. The default value is
                      "sqlite+aiosqlite:///users.sqlite3", which specifies an SQLite database stored in the file
                      "users.sqlite3".
    """
    dsn: AnyUrl = AnyUrl("sqlite+aiosqlite:///users.sqlite3")


