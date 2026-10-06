"""Tests for the ConfigGuard CLI."""

from typer.testing import CliRunner

from configguard.cli import app

runner = CliRunner()


def test_cli_help() -> None:
    """Verify that the CLI displays help information."""

    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Validate application configuration files" in result.stdout
    assert "validate" in result.stdout


def test_cli_version() -> None:
    """Verify that the CLI displays the application version."""

    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "0.1.0"


def test_validate_command_accepts_configuration_file() -> None:
    """Verify that the validate command accepts a configuration path."""

    result = runner.invoke(app, ["validate", "config.yaml"])

    assert result.exit_code == 0
    assert "Configuration file: config.yaml" in result.stdout