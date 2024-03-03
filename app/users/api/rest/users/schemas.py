from pydantic import BaseModel, constr, EmailStr
from app.common.api.schemas.paginated import PaginatedResponse

from app.users.api.rest.schemas import UserResponse


class UserUpdateRequest(BaseModel):
    """
    This class represents a request object for updating a user.

    Attributes:
    - username (constr): The new username for the user. This must be at least 1 character long and have no leading or trailing whitespace.
    - email (constr): The new email address for the user. This must be at least 1 character long and have no leading or trailing whitespace.
    """
    username: constr(strip_whitespace=True, min_length=1)
    email: constr(strip_whitespace=True, min_length=1)


class UserCreateRequest(BaseModel):
    """
    This class represents a request object for creating a new user.

    Attributes:
    - username (str): The username for the new user.
    - email (EmailStr): The email address for the new user.
    """
    username: str
    email: EmailStr


class UserListResponse(PaginatedResponse):
    """
    This class represents a response object for a list of users.

    Attributes:
    - data (list[UserResponse]): A list of UserResponse objects.
    """
    data: list[UserResponse]
