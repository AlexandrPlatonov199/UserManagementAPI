import os
import pathlib
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.users.database import Service
from app.users.database.models import User


def test_get_alembic_config_path(service: Service):
    expected_path = (
            pathlib.Path(os.curdir).absolute() / "app" / "users" / "database" / "migrations"
    )

    path = service.get_alembic_config_path()

    assert isinstance(path, pathlib.Path)
    assert path == expected_path


@pytest.mark.asyncio
async def test_get_user(service: Service):
    session = MagicMock()
    result = MagicMock()
    user_id = 1
    email = "test@gmail.com"

    result.unique().scalar_one_or_none.return_value = User(id=user_id, email=email)
    session.execute = AsyncMock()
    session.execute.return_value = result

    user = await service.get_user(
        session=session,
        email=email,
    )

    assert user is not None
    assert user.email == email


@pytest.mark.asyncio
async def test_create_user(service: Service):
    session = MagicMock()
    username = "Test"
    email = "test@gmail.com"

    user = await service.create_user(
        session=session,
        username=username,
        email=email,
    )

    assert user.email == email
    assert user.username == username


@pytest.mark.asyncio
async def test_update_user(service: Service):
    session = MagicMock()
    user = User(id=1, email="test@gmail.com", username="Test")

    new_username = "NewTest"
    new_email = "test@example.com"

    result_user = await service.update_user(
        session=session,
        user=user,
        username=new_username,
        email=new_email,
    )

    session.add.assert_called_once_with(user)
    assert user is result_user
    assert result_user.username == new_username
    assert result_user.email == new_email


@pytest.mark.asyncio
async def test_delete_user(service: Service):
    session = AsyncMock()
    user = User(id=1, email="test@gmail.com", username="Test")

    result_user = await service.delete_user(
        session=session,
        user=user
    )

    assert result_user.email == user.email
    assert result_user.username == user.username


@pytest.mark.asyncio
async def test_get_users_count_last_seven_days(service: Service):
    session = MagicMock()
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    result = MagicMock()
    result.scalar_one.return_value = 10

    session.execute = AsyncMock(return_value=result)

    user_count = await service.get_users_count_last_seven_days(
        session=session,
        seven_days_ago=seven_days_ago,
    )

    assert user_count == 10


@pytest.mark.asyncio
async def test_get_users_top_five_longest(service: Service):
    session = MagicMock()
    page = 1
    per_page = 5
    result = MagicMock()
    result.unique.return_value.scalars.return_value.all.return_value = [
        User(id=1, username="user1", email="user1@example.com"),
        User(id=2, username="user22", email="user2@example.com"),
        User(id=3, username="user333", email="user3@example.com"),
        User(id=4, username="user4444", email="user4@example.com"),
        User(id=5, username="user55555", email="user5@example.com"),
    ]

    session.execute = AsyncMock()
    session.execute.return_value = result

    users = await service.get_users_top_five_longest(
        session=session,
        page=page,
        per_page=per_page,
    )

    assert len(users) == per_page
    assert users[0].username == "user1"
    assert users[1].username == "user22"
    assert users[2].username == "user333"
    assert users[3].username == "user4444"
    assert users[4].username == "user55555"


@pytest.mark.asyncio
async def test_get_email_domain_ratio(service: Service):
    session = MagicMock()
    domain = "example.com"
    result = MagicMock()
    result.scalar_one_or_none.return_value = 0.5

    session.execute = AsyncMock(return_value=result)

    ratio = await service.get_email_domain_ratio(
        session=session,
        domain=domain,
    )

    assert ratio == 0.5


@pytest.mark.asyncio
async def test_get_user_count(service: Service):
    session = AsyncMock()
    total_users = 10

    # Mock the query result
    session.scalar.return_value = total_users

    # Call the function to test
    user_count = await service.get_user_count(
        session=session,
    )

    # Check that the function returned the correct value
    assert user_count == total_users
