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


def test_validate_command_rejects_missing_configuration_file(
    tmp_path: Path,
) -> None:
    """Verify that the validate command rejects a missing file."""

    config_file = tmp_path / "missing.yaml"

    result = runner.invoke(app, ["validate", str(config_file)])

    assert result.exit_code == 2
    assert f"Configuration file does not exist: {config_file}" in result.stderr


def test_validate_command_rejects_invalid_configuration_file(
    tmp_path: Path,
) -> None:
    """Verify that the validate command rejects invalid configuration data."""

    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        "application: [invalid",
        encoding="utf-8",
    )

    result = runner.invoke(app, ["validate", str(config_file)])

    assert result.exit_code == 2
    assert "Invalid YAML configuration" in result.stderr


def test_validate_command_accepts_valid_configuration(
    tmp_path: Path,
) -> None:
    """Verify that the CLI accepts a valid configuration."""

    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
application:
  name: payment-api
  environment: production
server:
  host: 0.0.0.0
  port: 8080
database:
  host: db.internal
  name: payments
  username: payment_user
logging:
  level: INFO
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["validate", str(config_file)])

    assert result.exit_code == 0
    assert result.stdout.strip() == "Configuration is valid."


def test_validate_command_rejects_invalid_configuration(
    tmp_path: Path,
) -> None:
    """Verify that the CLI rejects an invalid configuration."""

    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
application:
  name: payment-api
  environment: production
server:
  host: 0.0.0.0
  port: 70000
database:
  host: db.internal
  name: payments
  username: payment_user
logging:
  level: INFO
""".strip(),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["validate", str(config_file)])

    assert result.exit_code == 1
    assert result.stderr.strip() == "Configuration is invalid."