import typer

from app.common.database.cli import get_migrations_cli
from app.common.utils.settings import get_settings

from .service import get_service
from .settings import Settings


def callback(ctx: typer.Context):
    """Callback function for the CLI.

    This function sets up the database service and settings in the context object.

    Args:
        ctx (typer.Context): The context object to store the database service and settings in.
    """
    ctx.obj = ctx.obj or {}

    if settings := ctx.obj.get("settings"):
        settings = settings.database
    else:
        settings = get_settings(Settings)
    database_service = get_service(settings=settings)

    ctx.obj["settings"] = settings
    ctx.obj["database"] = database_service


def get_cli() -> typer.Typer:
    """Create and configure the CLI.

    This function creates an instance of the `typer.Typer` class, sets up the callback function to be called when the
    CLI is invoked, and adds the `migrations` command to the CLI.

    Returns:
        An instance of the `typer.Typer` class.
    """
    cli = typer.Typer(name="Database")

    cli.callback()(callback)
    cli.add_typer(get_migrations_cli(), name="migrations")

    return cli
