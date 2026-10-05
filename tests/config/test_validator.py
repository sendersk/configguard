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


def test_validate_configuration_preserves_validation_errors() -> None:
    """Verify that structured validation errors are preserved."""

    data = valid_configuration()
    data["server"]["port"] = 70000

    with pytest.raises(ConfigurationValidationError) as exc_info:
        validate_configuration(data)

    assert exc_info.value.errors
    assert exc_info.value.errors[0]["loc"] == ("server", "port")


def test_validate_configuration_preserves_multiple_errors() -> None:
    """Verify that multiple validation errors are preserved."""

    data = valid_configuration()
    data["application"]["name"] = ""
    data["server"]["port"] = 70000
    data["database"]["host"] = ""

    with pytest.raises(ConfigurationValidationError) as exc_info:
        validate_configuration(data)

    errors = exc_info.value.errors

    assert len(errors) == 3
    assert {error["loc"] for error in errors} == {
        ("application", "name"),
        ("server", "port"),
        ("database", "host"),
    }


def test_validate_configuration_error_contains_message() -> None:
    """Verify that validation errors contain human-readable messages."""

    data = valid_configuration()
    data["server"]["port"] = 70000

    with pytest.raises(ConfigurationValidationError) as exc_info:
        validate_configuration(data)

    error = exc_info.value.errors[0]

    assert "port" in str(error["loc"])
    assert "less than or equal to 65535" in str(error["msg"])


def test_validate_configuration_error_contains_error_type() -> None:
    """Verify that validation errors contain error types."""

    data = valid_configuration()
    data["application"]["environment"] = "invalid"

    with pytest.raises(ConfigurationValidationError) as exc_info:
        validate_configuration(data)

    error = exc_info.value.errors[0]

    assert error["loc"] == ("application", "environment")
    assert error["type"] == "literal_error"


@pytest.mark.parametrize(
    "host",
    [
        "localhost",
        "127.0.0.1",
    ],
)
def test_validate_configuration_rejects_localhost_in_production(
    host: str,
) -> None:
    """Verify that production cannot use localhost as the server host."""

    data = valid_configuration()
    data["application"]["environment"] = "production"
    data["server"]["host"] = host

    with pytest.raises(
        ConfigurationValidationError,
        match="Configuration validation failed",
    ):
        validate_configuration(data)


@pytest.mark.parametrize(
    "environment",
    [
        "development",
        "testing",
        "staging",
    ],
)
def test_validate_configuration_allows_localhost_outside_production(
    environment: str,
) -> None:
    """Verify that localhost is allowed outside production."""

    data = valid_configuration()
    data["application"]["environment"] = environment
    data["server"]["host"] = "localhost"

    result = validate_configuration(data)

    assert result.server.host == "localhost"


@pytest.mark.parametrize(
    "host",
    [
        "localhost",
        "127.0.0.1",
    ],
)
def test_validate_configuration_reports_production_host_error(
    host: str,
) -> None:
    """Verify that production host validation reports a structured error."""

    data = valid_configuration()
    data["application"]["environment"] = "production"
    data["server"]["host"] = host

    with pytest.raises(ConfigurationValidationError) as exc_info:
        validate_configuration(data)

    errors = exc_info.value.errors

    assert len(errors) == 1
    assert errors[0]["type"] == "value_error"
    assert (
        "Production applications must not use localhost"
        in str(errors[0]["msg"])
    )