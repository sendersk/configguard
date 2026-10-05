"""Tests for configuration validation."""

from typing import Any

import pytest

from configguard.config.models import AppConfig
from configguard.config.validator import (
    ConfigurationValidationError,
    validate_configuration,
)


def valid_configuration() -> dict[str, Any]:
    """Return a valid raw configuration."""

    return {
        "application": {
            "name": "payment-api",
            "environment": "production",
        },
        "server": {
            "host": "0.0.0.0",
            "port": 8080,
        },
        "database": {
            "host": "db.internal",
            "name": "payments",
            "username": "payment_user",
        },
        "logging": {
            "level": "INFO",
        },
    }


def test_validate_configuration_returns_app_config() -> None:
    """Verify that valid data is converted to AppConfig."""

    result = validate_configuration(valid_configuration())

    assert isinstance(result, AppConfig)
    assert result.application.name == "payment-api"
    assert result.server.port == 8080
    assert result.database.port == 5432
    assert result.logging.level.value == "INFO"


def test_validate_configuration_rejects_missing_application() -> None:
    """Verify that a missing application section is rejected."""

    data = valid_configuration()
    del data["application"]

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


def test_validate_configuration_rejects_missing_server() -> None:
    """Verify that a missing server section is rejected."""

    data = valid_configuration()
    del data["server"]

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


def test_validate_configuration_rejects_missing_database() -> None:
    """Verify that a missing database section is rejected."""

    data = valid_configuration()
    del data["database"]

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


def test_validate_configuration_rejects_missing_logging() -> None:
    """Verify that a missing logging section is rejected."""

    data = valid_configuration()
    del data["logging"]

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


def test_validate_configuration_rejects_invalid_server_port() -> None:
    """Verify that an invalid server port is rejected."""

    data = valid_configuration()
    data["server"]["port"] = 70000

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


@pytest.mark.parametrize(
    "environment",
    [
        "local",
        "development2",
        "prod",
        "",
    ],
)
def test_validate_configuration_rejects_invalid_environment(
    environment: str,
) -> None:
    """Verify that unsupported environments are rejected."""

    data = valid_configuration()
    data["application"]["environment"] = environment

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


@pytest.mark.parametrize(
    "port",
    [
        0,
        -1,
        65536,
        100000,
    ],
)
def test_validate_configuration_rejects_invalid_server_ports(
    port: int,
) -> None:
    """Verify that invalid server ports are rejected."""

    data = valid_configuration()
    data["server"]["port"] = port

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


def test_validate_configuration_rejects_empty_application_name() -> None:
    """Verify that an empty application name is rejected."""

    data = valid_configuration()
    data["application"]["name"] = ""

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


def test_validate_configuration_rejects_empty_server_host() -> None:
    """Verify that an empty server host is rejected."""

    data = valid_configuration()
    data["server"]["host"] = ""

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


@pytest.mark.parametrize(
    "port",
    [
        0,
        -1,
        65536,
        100000,
    ],
)
def test_validate_configuration_rejects_invalid_database_ports(
    port: int,
) -> None:
    """Verify that invalid database ports are rejected."""

    data = valid_configuration()
    data["database"]["port"] = port

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


def test_validate_configuration_rejects_empty_database_host() -> None:
    """Verify that an empty database host is rejected."""

    data = valid_configuration()
    data["database"]["host"] = ""

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


@pytest.mark.parametrize(
    "level",
    [
        "TRACE",
        "trace",
        "INVALID",
        "",
    ],
)
def test_validate_configuration_rejects_invalid_log_level(
    level: str,
) -> None:
    """Verify that unsupported logging levels are rejected."""

    data = valid_configuration()
    data["logging"]["level"] = level

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)