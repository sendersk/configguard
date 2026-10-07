"""Command-line interface for ConfigGuard."""

from importlib.metadata import version
from pathlib import Path

import typer

from configguard.config.loader import ConfigurationLoadError, load_configuration
from configguard.config.validator import (
    ConfigurationValidationError,
    validate_configuration,
)


def version_callback(value: bool) -> None:
    """Display the application version and exit."""

    if value:
        typer.echo(version("configguard"))
        raise typer.Exit()

app = typer.Typer(
    name="configguard",
    help="Validate application configuration files before deployment.",
)


@app.callback()
def main(
    version_option: bool = typer.Option(
        False,
        "--version",
        help="Show the application version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Validate application configuration files before deployment."""

    if version_option:
        typer.echo(version("configguard"))
        raise typer.Exit()


config_file_argument = typer.Argument(
    ...,
    help="Path to the configuration file.",
)


@app.command()
def validate(
    config_file: Path = config_file_argument,
) -> None:
    """Validate a configuration file."""

    if not config_file.is_file():
        typer.echo(
            f"Configuration file does not exist: {config_file}",
            err=True,
        )
        raise typer.Exit(code=2)

    try:
        data = load_configuration(config_file)
    except ConfigurationLoadError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=2) from error

    try:
        validate_configuration(data)
    except ConfigurationValidationError:
        typer.echo("Configuration is invalid.", err=True)
        raise typer.Exit(code=1)

    typer.echo("Configuration is valid.")