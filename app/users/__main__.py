"""Entry point for the app.users command line interface (CLI).

This module defines the entry point for the CLI of the app.users package. It imports the get_cli function from
the cli module and creates a typer.Typer object that represents the CLI. The CLI is then invoked by calling the
typer.Typer object as a function.
"""
from .cli import get_cli

if __name__ == "__main__":
    cli = get_cli()

    cli()