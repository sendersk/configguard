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
        }
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