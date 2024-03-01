from pydantic import BaseModel, constr, EmailStr


class UserUpdateRequest(BaseModel):
    """A request object for updating a user.

    Attributes:
        username (constr): The new username for the user. Must be at least 1 character long and have no leading or
            trailing whitespace.
        email (constr): The new email address for the user. Must be at least 1 character long and have no leading or
            trailing whitespace.
    """
    username: constr(strip_whitespace=True, min_length=1)
    email: constr(strip_whitespace=True, min_length=1)


class UserCreateRequest(BaseModel):
    """A request object for creating a new user.

    Attributes:
        username (str): The username for the new user.
        email (EmailStr): The email address for the new user.
    """
    username: str
    email: EmailStr

