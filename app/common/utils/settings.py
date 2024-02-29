import os
import pathlib
from typing import Type, TypeVar

from pydantic_settings import BaseSettings, SettingsConfigDict

Settings = TypeVar("Settings")

def get_settings(settings_cls: Type[Settings], env_file: pathlib.Path | None = None) -> Settings:
    """Create and configure the settings for the application.

    This function reads environment variables and values from an `.env` file to configure the settings for the
    application. If a `secrets_dir` is present, it will also read values from files in that directory and set them as
    environment variables.

    Args:
        settings_cls (Type[Settings]): The settings class to use. This should be a subclass of `BaseSettings`.
        env_file (pathlib.Path | None): The path to the `.env` file. If not provided, the default `.env` file will be
                                       used.

    Returns:
        An instance of the `settings_cls` class, configured with the values read from the environment variables and `.env`
        file.
    """
    secrets_dir = pathlib.Path("/run/secrets")
    if secrets_dir.is_dir():
        for secret_file in secrets_dir.iterdir():
            if not secret_file.is_file():
                continue

            os.environ[secret_file.name] = secret_file.read_text().strip()

    return type(
        "Settings",
        (settings_cls, BaseSettings),
        {
            "model_config": SettingsConfigDict(
                env_nested_delimiter="__",
                env_file=None if env_file is None else str(env_file),
                extra="ignore",
                secrets_dir=str(secrets_dir),
            ),
        },
    )()
