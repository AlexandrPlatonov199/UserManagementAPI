"""
CLI module for user management.

This module provides a command-line interface for managing users in the application. It defines a `run` command
that starts the user service, and includes a subcommand for managing the database.
"""

import asyncio

import typer
from loguru import logger

from app.common.utils.settings import get_settings

from . import database
from .service import get_service
from .settings import Settings

@logger.catch
def run(ctx: typer.Context):
    """
    Start the user service.

    Args:
        ctx (typer.Context): The context object containing information about the current execution context.
    """
    loop: asyncio.AbstractEventLoop = ctx.obj["loop"]
    settings: Settings = ctx.obj["settings"]

    users_service = get_service(settings=settings)

    loop.run_until_complete(users_service.run())

def callback(ctx: typer.Context):
    """
    Set up the context object with default values for the event loop and settings.

    Args:
        ctx (typer.Context): The context object containing information about the current execution context.
    """
    ctx.obj = ctx.obj or {}

    if "loop" not in ctx.obj:
        ctx.obj["loop"] = asyncio.get_event_loop()

    if settings := ctx.obj.get("settings"):
        ctx.obj["settings"] = settings.users
    else:
        ctx.obj["settings"] = get_settings(Settings)

def get_cli() -> typer.Typer:
    """
    Create and return the CLI object for user management.

    Returns:
        typer.Typer: The CLI object.
    """
    cli = typer.Typer()

    cli.callback()(callback)
    cli.command(name="run")(run)
    cli.add_typer(database.get_cli(), name="database")

    return cli