from pydantic import BaseModel

from .users import Settings as UsersSettings


class Settings(BaseModel):
    """Settings class for the application.

    This class is used to represent the settings required by the application, including the settings for the user
    service.

    Attributes:
        users (UsersSettings): The settings for the user service.
    """
    users: UsersSettings = UsersSettings()
