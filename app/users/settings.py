from pydantic import BaseModel

from .api import Settings as APISettings
from .database import Settings as DatabaseSettings


class Settings(BaseModel):
    """Settings class for the application.

    This class is used to represent the settings required by the application, including the settings for the API and
    database.

    Attributes:
        api (APISettings): The settings for the API.
        database (DatabaseSettings): The settings for the database.
    """
    api: APISettings = APISettings()
    database: DatabaseSettings = DatabaseSettings()