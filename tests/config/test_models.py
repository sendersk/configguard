"""Tests for configuration models."""

import pytest
from pydantic import ValidationError

from configguard.config.models import AppConfig


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
            }
        )


def test_app_config_rejects_invalid_environment() -> None:
    """Verify that an unsupported environment is rejected."""

    with pytest.raises(ValidationError):
        AppConfig(
            application={
                "name": "payment-api",
                "environment": "prod",
            }
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
        )