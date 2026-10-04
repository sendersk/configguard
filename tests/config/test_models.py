"""Tests for configuration models."""

import pytest
from pydantic import ValidationError

from configguard.config.models import AppConfig, LoggingConfig, LogLevel


def valid_database_configuration() -> dict[str, object]:
    """Return a valid database configuration."""

    return {
        "host": "db.internal",
        "name": "payments",
        "username": "payment_user",
    }


def valid_logging_configuration() -> dict[str, str]:
    """Return a valid logging configuration."""

    return {"level": "INFO"}


def test_app_config_accepts_valid_configuration() -> None:
    """Verify that a valid configuration is accepted."""

    config = AppConfig(
        application={
            "name": "payment-api",
            "environment": "production",
        },
        server={
            "host": "0.0.0.0",
            "port": 8080,
        },
        database=valid_database_configuration(),
        logging=valid_logging_configuration(),
    )

    assert config.application.name == "payment-api"
    assert config.application.environment == "production"


def test_app_config_rejects_empty_application_name() -> None:
    """Verify that an empty application name is rejected."""

    with pytest.raises(ValidationError):
        AppConfig(
            application={
                "name": "",
                "environment": "production",
            },
            database=valid_database_configuration(),
            logging=valid_logging_configuration(),
        )


def test_app_config_rejects_invalid_environment() -> None:
    """Verify that an unsupported environment is rejected."""

    with pytest.raises(ValidationError):
        AppConfig(
            application={
                "name": "payment-api",
                "environment": "prod",
            },
            database=valid_database_configuration(),
            logging=valid_logging_configuration(),
        )


def test_app_config_accepts_valid_server_configuration() -> None:
    """Verify that a valid server configuration is accepted."""

    config = AppConfig(
        application={
            "name": "payment-api",
            "environment": "production",
        },
        server={
            "host": "0.0.0.0",
            "port": 8080,
        },
        database=valid_database_configuration(),
        logging=valid_logging_configuration(),
    )

    assert config.server.host == "0.0.0.0"
    assert config.server.port == 8080


@pytest.mark.parametrize("port", [0, -1, 65536, 100000])
def test_app_config_rejects_invalid_server_port(port: int) -> None:
    """Verify that an invalid server port is rejected."""

    with pytest.raises(ValidationError):
        AppConfig(
            application={
                "name": "payment-api",
                "environment": "production",
            },
            server={
                "host": "0.0.0.0",
                "port": port,
            },
            database=valid_database_configuration(),
            logging=valid_logging_configuration(),
        )


def test_app_config_rejects_empty_server_host() -> None:
    """Verify that an empty server host is rejected."""

    with pytest.raises(ValidationError):
        AppConfig(
            application={
                "name": "payment-api",
                "environment": "production",
            },
            server={
                "host": "",
                "port": 8080,
            },
            database=valid_database_configuration(),
            logging=valid_logging_configuration(),
        )


def test_app_config_accepts_valid_database_configuration() -> None:
    """Verify that a valid database configuration is accepted."""

    config = AppConfig(
        application={
            "name": "payment-api",
            "environment": "production",
        },
        server={
            "host": "0.0.0.0",
            "port": 8080,
        },
        database=valid_database_configuration(),
        logging=valid_logging_configuration(),
    )

    assert config.database.host == "db.internal"
    assert config.database.port == 5432
    assert config.database.name == "payments"
    assert config.database.username == "payment_user"
    assert config.database.password is None


def test_database_port_defaults_to_postgresql_port() -> None:
    """Verify that the default database port is PostgreSQL's standard port."""

    config = AppConfig(
        application={
            "name": "payment-api",
            "environment": "production",
        },
        server={
            "host": "0.0.0.0",
            "port": 8080,
        },
        database=valid_database_configuration(),
        logging=valid_logging_configuration(),
    )

    assert config.database.port == 5432


@pytest.mark.parametrize("port", [0, -1, 65536, 100000])
def test_app_config_rejects_invalid_database_port(port: int) -> None:
    """Verify that an invalid database port is rejected."""

    database = valid_database_configuration()
    database["port"] = port

    with pytest.raises(ValidationError):
        AppConfig(
            application={
                "name": "payment-api",
                "environment": "production",
            },
            server={
                "host": "0.0.0.0",
                "port": 8080,
            },
            database=database,
            logging=valid_logging_configuration(),
        )


def test_app_config_rejects_empty_database_host() -> None:
    """Verify that an empty database host is rejected."""

    database = valid_database_configuration()
    database["host"] = ""

    with pytest.raises(ValidationError):
        AppConfig(
            application={
                "name": "payment-api",
                "environment": "production",
            },
            server={
                "host": "0.0.0.0",
                "port": 8080,
            },
            database=database,
            logging=valid_logging_configuration(),
        )


def test_app_config_accepts_valid_logging_configuration() -> None:
    """Verify that a valid logging configuration is accepted."""

    config = AppConfig(
        application={
            "name": "payment-api",
            "environment": "production",
        },
        server={
            "host": "0.0.0.0",
            "port": 8080,
        },
        database=valid_database_configuration(),
        logging=valid_logging_configuration(),
    )

    assert config.logging.level == LogLevel.INFO


def test_logging_level_defaults_to_info() -> None:
    """Verify that the default logging level is INFO."""

    config = LoggingConfig()

    assert config.level == LogLevel.INFO


@pytest.mark.parametrize(
    "level",
    ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
)
def test_logging_config_accepts_supported_level(level: str) -> None:
    """Verify that all supported logging levels are accepted."""

    config = LoggingConfig(level=level)

    assert config.level.value == level


def test_logging_config_rejects_unsupported_level() -> None:
    """Verify that an unsupported logging level is rejected."""

    with pytest.raises(ValidationError):
        LoggingConfig(level="TRACE")