"""Configuration validation utilities."""

from typing import Any

from pydantic import ValidationError

from configguard.config.models import AppConfig


class ConfigurationValidationError(Exception):
    """Raised when configuration data is invalid."""


def validate_configuration(data: dict[str, Any]) -> AppConfig:
    """Validate configuration data against the application model.

    Args:
        data: Raw configuration data.

    Returns:
        Validated application configuration.

    Raises:
        ConfigurationValidationError: If the configuration is invalid.
    """

    try:
        return AppConfig.model_validate(data)
    except ValidationError as error:
        raise ConfigurationValidationError(
            "Configuration validation failed."
        ) from error