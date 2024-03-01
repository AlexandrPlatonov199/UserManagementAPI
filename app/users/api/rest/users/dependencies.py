import fastapi

from app.common.api.exceptions import HTTPNotFound
from app.users import database
from app.users.database.models import User


async def get_path_user(
        request: fastapi.Request,
        user_id: int = fastapi.Path(),
) -> User:
    """Get a user object from the database by ID.

    Args:
        request (fastapi.Request): The FastAPI request object.
        user_id (int): The ID of the user to retrieve.

    Returns:
        The user object with the specified ID, or raises an `HTTPNotFound` exception if the user is not found.
    """
    database_service: database.Service = request.app.service.database

    async with database_service.transaction() as session:
        db_user = await database_service.get_user(session=session, user_id=user_id)
    if db_user is None:
        raise HTTPNotFound()

    return db_user
