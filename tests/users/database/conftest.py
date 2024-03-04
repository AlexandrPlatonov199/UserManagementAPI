import pytest

from app.common.utils.settings import get_settings
from app.users.database import Service, Settings


@pytest.fixture()
def settings() -> Settings:
    return get_settings(Settings)


@pytest.fixture()
def service(settings: Settings) -> Service:
    return Service(dsn=str(settings.dsn))
