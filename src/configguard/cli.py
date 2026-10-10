"""Command-line interface for ConfigGuard."""

import logging
from importlib.metadata import version
from pathlib import Path
from typing import Literal

import typer

from configguard.config.loader import ConfigurationLoadError, load_configuration
from configguard.config.result import ValidationResult
from configguard.config.validator import (
    ConfigurationValidationError,
    validate_configuration,
    validate_strict_configuration,
)
from configguard.logging import configure_logging
from configguard.output.human import format_human_result
from configguard.output.json import format_json_result


def version_callback(value: bool) -> None:
    """Display the application version and exit."""

    if value:
        typer.echo(version("configguard"))
        raise typer.Exit()

app = typer.Typer(
    name="configguard",
    help="Validate application configuration files before deployment.",
)
logger = logging.getLogger(__name__)


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

output_format_option = typer.Option(
    "human",
    "--format",
    help="Output format.",
)

strict_option = typer.Option(
    False,
    "--strict",
    help="Enable strict validation.",
)


@app.command()
def validate(
    config_file: Path = config_file_argument,
    output_format: Literal["human", "json"] = output_format_option,
    strict: bool = strict_option,
) -> None:
    """Validate a configuration file."""

    configure_logging()
    logger.debug("Starting configuration validation.")

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
        config = validate_configuration(data)

        if strict:
            validate_strict_configuration(config)

    except ConfigurationValidationError as error:
        result = ValidationResult.from_errors(error.errors)
        exit_code = 1
    else:
        result = ValidationResult(valid=True)
        exit_code = 0

    logger.debug("Configuration file loaded: %s", config_file)

    if output_format == "json":
        typer.echo(format_json_result(result))
    else:
        typer.echo(format_human_result(result))

    if result.valid:
        logger.debug("Configuration validation succeeded.")
    else:
        logger.debug("Configuration validation failed.")

    raise typer.Exit(code=exit_code)

