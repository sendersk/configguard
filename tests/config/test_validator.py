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