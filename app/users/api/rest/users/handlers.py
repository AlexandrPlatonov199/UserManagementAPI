from datetime import datetime, timedelta

import fastapi

from app.common.api.dependencies.pagination import Pagination, pagination
from app.users import database
from app.users.api.rest.schemas import UserResponse
from app.users.database.models import User

from .dependencies import get_path_user, predict_user_activity
from .schemas import UserCreateRequest, UserListResponse, UserUpdateRequest


async def get_user(
        user: User = fastapi.Depends(get_path_user),
) -> UserResponse:
    """Get a user by ID.

    Args:
        user (User): The user object, retrieved from the database using the `get_path_user` dependency.

    Returns:
        A `UserResponse` object with the user's data.
    """
    activity_probability = await predict_user_activity(user)
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        updated_registration_date=user.updated_registration_date,
        registration_date=user.registration_date,
        activity_probability=activity_probability
    )


async def get_users(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
) -> UserListResponse:
    """Retrieve a list of users.

    Args:
        request (fastapi.Request): The FastAPI request object.
        pagination (Pagination, optional): The pagination settings. Defaults to fastapi.Depends(pagination).

    Returns:
        A `UserListResponse` object with a list of `UserResponse` objects, pagination details, and the total number of users.
    """
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        users_db = await database_service.get_users(
            session=session,
            page=pagination.page,
            per_page=pagination.per_page,
        )
        total_users = await database_service.get_user_count(session)

    total_pages = -(total_users // -pagination.per_page)
    users = [UserResponse(id=user_db.id,
                          username=user_db.username,
                          email=user_db.email,
                          registration_date=user_db.registration_date,
                          updated_registration_date=user_db.updated_registration_date,
                          activity_probability=None) for user_db in users_db]

    return UserListResponse(
        data=users,
        page=pagination.page,
        per_page=pagination.per_page,
        total_items=total_users,
        total_pages=total_pages,
    )


async def get_users_count_last_seven_days(
    request: fastapi.Request,
) -> int:
    """
    Get the number of users who registered in the last seven days.

    Args:
        request: The FastAPI request object.

    Returns:
        The number of users who registered in the last seven days.
    """
    database_service: database.Service = request.app.service.database

    seven_days_ago = datetime.now() - timedelta(days=7)
    async with database_service.transaction() as session:
        users_db = await database_service.get_users_count_last_seven_days(
            session=session,
            seven_days_ago=seven_days_ago,
        )

    return users_db


async def get_users_top_five_longest(
    request: fastapi.Request,
    pagination: Pagination = fastapi.Depends(pagination),
) -> UserListResponse:
    """
    Get a paginated list of the top five users with the longest registration dates.

    Args:
        request: The FastAPI request object.
        pagination: An optional pagination object. Defaults to the global pagination settings.

    Returns:
        A `UserListResponse` object containing a list of the top five users with the longest registration dates,
        as well as pagination metadata.
    """
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        users_db = await database_service.get_users_top_five_longest(
            session=session,
            page=pagination.page,
            per_page=pagination.per_page,
        )
        total_users = await database_service.get_user_count(session)

    total_pages = -(total_users // -pagination.per_page)
    users = [UserResponse.model_validate(user_db) for user_db in users_db]

    return UserListResponse(
        data=users,
        page=pagination.page,
        per_page=pagination.per_page,
        total_items=total_users,
        total_pages=total_pages,
    )


async def get_email_domain_ratio(
    request: fastapi.Request,
) -> float:
    """
    Get the ratio of users with email addresses from a specific domain.

    Args:
        request: The FastAPI request object.

    Returns:
        A float representing the ratio of users with email addresses from the specified domain.
    """
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        users_db = await database_service.get_email_domain_ratio(
            session=session,
            domain="example.com"
        )

    return users_db


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
