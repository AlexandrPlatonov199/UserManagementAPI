import fastapi

from app.users import database
from app.users.api.rest.schemas import UserResponse
from app.users.database.models import User

from .dependencies import get_path_user
from .schemas import UserUpdateRequest, UserCreateRequest


async def get_user(
        user: User = fastapi.Depends(get_path_user),
) -> UserResponse:
    """Get a user by ID.

    Args:
        user (User): The user object, retrieved from the database using the `get_path_user` dependency.

    Returns:
        A `UserResponse` object with the user's data.
    """
    return UserResponse.from_db_model(user)


async def create_user(
    request: fastapi.Request,
    data: UserCreateRequest = fastapi.Body(embed=False),
) -> UserResponse:
    """Create a new user.

    Args:
        request (fastapi.Request): The FastAPI request object.
        data (UserCreateRequest): The user data, sent in the request body.

    Returns:
        A `UserResponse` object with the new user's data.
    """
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        user = await database_service.create_user(
            session=session,
            username=data.username,
            email=data.email
        )

    return UserResponse.from_db_model(user)


async def update_user(
        request: fastapi.Request,
        user: User = fastapi.Depends(get_path_user),
        data: UserUpdateRequest = fastapi.Body(embed=False),
) -> UserResponse:
    """Update a user's data.

    Args:
        request (fastapi.Request): The FastAPI request object.
        user (User): The user object, retrieved from the database using the `get_path_user` dependency.
        data (UserUpdateRequest): The user data, sent in the request body.

    Returns:
        A `UserResponse` object with the updated user's data.
    """
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        user = await database_service.update_user(
            user=user,
            session=session,
            username=data.username,
            email=data.email,

        )

    return UserResponse.from_db_model(user)


async def delete_user(
        request: fastapi.Request,
        user: User = fastapi.Depends(get_path_user),
) -> UserResponse:
    """Delete a user.

    Args:
        request (fastapi.Request): The FastAPI request object.
        user (User): The user object, retrieved from the database using the `get_path_user` dependency.

    Returns:
        A `UserResponse` object with the deleted user's data.
    """
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        user = await database_service.delete_user(
            session=session,
            user=user,
        )

    return UserResponse.from_db_model(user)
