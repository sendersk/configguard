"""Command-line interface for ConfigGuard."""

from importlib.metadata import version

import typer

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
    ),
) -> None:
    """Validate application configuration files before deployment."""

    if version_option:
        typer.echo(version("configguard"))
        raise typer.Exit()


@app.command()
def validate(
    config_file: str = typer.Argument(
        ...,
        help="Path to the configuration file.",
    ),
) -> None:
    """Validate a configuration file."""

    typer.echo(f"Configuration file: {config_file}")