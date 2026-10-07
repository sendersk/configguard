"""Tests for the ConfigGuard CLI."""
from pathlib import Path

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


def test_validate_command_accepts_configuration_file(
    tmp_path: Path,
) -> None:
    """Verify that the validate command accepts an existing file."""

    config_file = tmp_path / "config.yaml"
    config_file.write_text("application: {}", encoding="utf-8")

    result = runner.invoke(app, ["validate", str(config_file)])

    assert result.exit_code == 0
    assert f"Configuration file: {config_file}" in result.stdout


def test_validate_command_rejects_missing_configuration_file(
    tmp_path: Path,
) -> None:
    """Verify that the validate command rejects a missing file."""

    config_file = tmp_path / "missing.yaml"

    result = runner.invoke(app, ["validate", str(config_file)])

    assert result.exit_code == 2
    assert f"Configuration file does not exist: {config_file}" in result.stderr