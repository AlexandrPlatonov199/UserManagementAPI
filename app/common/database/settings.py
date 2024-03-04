from pydantic import AnyUrl, BaseModel


class BaseDatabaseSettings(BaseModel):
    """
    Base class for defining database settings.

    Attributes:
        dsn (AnyUrl): The URL of the database connection string.
    """
    dsn: AnyUrl