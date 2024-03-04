import pytest

from app.common.utils.settings import get_settings
from app.users import Settings


@pytest.fixture()
def settings() -> Settings:
    return get_settings(Settings)
