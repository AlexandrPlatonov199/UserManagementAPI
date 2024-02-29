from typing import Optional

import typer

from .service import BaseDatabaseService


def migrations_list(ctx: typer.Context):
    """
    Shows a list of database migrations.
    """
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.show_migrations()


def migrations_apply(ctx: typer.Context):
    """
    Applies all pending database migrations.
    """
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.migrate()


def migrations_rollback(
    ctx: typer.Context,
    revision: Optional[str] = typer.Argument(
        None,
        help="Revision id or relative revision (`-1`, `-2`)",
    ),
):
    """
    Rolls back the database to a specified revision.

    Args:
        revision (str, optional): The revision to roll back to. Defaults to None.
    """
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.rollback(revision=revision)


def migrations_create(
    ctx: typer.Context,
    message: Optional[str] = typer.Option(
        None,
        "-m", "--message",
        help="Migration short message",
    ),
):
    """
    Creates a new database migration with a specified message.

    Args:
        message (str, optional): The message for the migration. Defaults to None.
    """
    database_service: BaseDatabaseService = ctx.obj["database"]

    database_service.create_migration(message=message)


def get_migrations_cli() -> typer.Typer:
    """
    Returns a Typer CLI object for managing database migrations.

    Returns:
        typer.Typer: A Typer CLI object for managing database migrations.
    """
    cli = typer.Typer(name="Migration")

    cli.command(name="apply")(migrations_apply)
    cli.command(name="rollback")(migrations_rollback)
    cli.command(name="create")(migrations_create)
    cli.command(name="list")(migrations_list)

    return cli
