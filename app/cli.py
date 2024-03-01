import asyncio
import pathlib
from typing import Optional

import typer
from loguru import logger

from app.common.utils.settings import get_settings

from . import users
from .service import get_service
from .settings import Settings


@logger.catch
def run(ctx: typer.Context):
    """Run the application.

    This function retrieves the event loop and settings from the context, creates an instance of the service, and runs
    the service.

    Args:
        ctx (typer.Context): The context object containing the event loop and settings.
    """
    loop: asyncio.AbstractEventLoop = ctx.obj["loop"]
    settings: Settings = ctx.obj["settings"]

    users_service = get_service(loop=loop, settings=settings)

    loop.run_until_complete(users_service.run())


def callback(
        ctx: typer.Context,
        env: Optional[pathlib.Path] = typer.Option(
            None,
            "--env", "-e",
            help="`.env` config file location",
        ),
):
    """Callback function for the CLI.

    This function sets up the event loop and settings in the context object.

    Args:
        ctx (typer.Context): The context object to store the event loop and settings in.
        env (Optional[pathlib.Path]): The path to the `.env` config file. If not provided, the default settings will
                                      be used.
    """
    ctx.obj = ctx.obj or {}

    if "loop" not in ctx.obj:
        ctx.obj["loop"] = asyncio.get_event_loop()

    if settings := ctx.obj.get("settings"):
        ctx.obj["settings"] = settings.sapphire
    else:
        ctx.obj["settings"] = get_settings(Settings, env_file=env)

def get_cli() -> typer.Typer:
    """Create and configure the CLI.

    This function creates an instance of the `typer.Typer` class, sets up the callback function to be called when the
    CLI is invoked, and adds the `run` and `users` commands to the CLI.

    Returns:
        An instance of the `typer.Typer` class.
    """
    cli = typer.Typer()

    cli.callback()(callback)
    cli.command(name="run")(run)
    cli.add_typer(users.get_cli(), name="users")

    return cli
