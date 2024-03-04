import pytest

from app import Settings
from app.common.utils.settings import get_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings(Settings)
