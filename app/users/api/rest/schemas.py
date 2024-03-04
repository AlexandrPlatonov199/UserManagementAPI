from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr
from app.users.database.models import User


class UserResponse(BaseModel):
    """A response object representing a user.

    Attributes:
        id (int): The ID of the user.
        username (str): The username of the user.
        email (EmailStr): The email address of the user.
        updated_registration_date (datetime): The date and time the user's registration was last updated.
        registration_date (datetime): The date and time the user registered.
    """
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    updated_registration_date: datetime
    registration_date: datetime
    activity_probability: float | None = None

    @classmethod
    def from_db_model(cls, user: User) -> "UserResponse":
        """Create a UserResponse object from a User database model.

        Args:
            user (User): The User database model.

        Returns:
            A UserResponse object.
        """
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            registration_date=user.registration_date,
            updated_registration_date=user.updated_registration_date,
            activity_probability=None
        )
