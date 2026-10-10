
"""Configuration validation utilities."""

from typing import Any

from pydantic import ValidationError
from pydantic_core import ErrorDetails, PydanticCustomError

from configguard.config.models import AppConfig


class ConfigurationValidationError(Exception):
    """Raised when configuration data is invalid."""

    def __init__(self, errors: list[ErrorDetails]) -> None:
        """Initialize a configuration validation error.

        Args:
            errors: Structured validation errors.
        """
        super().__init__("Configuration validation failed.")
        self.errors = errors


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
        raise ConfigurationValidationError(error.errors()) from error



def validate_strict_configuration(config: AppConfig) -> None:
    """Validate additional strict configuration rules.

    Args:
        config: Validated application configuration.

    Raises:
        ConfigurationValidationError: If strict validation fails.
    """

    if (
        config.application.environment == "production"
        and not config.database.password
    ):
        error = ValidationError.from_exception_data(
            "AppConfig",
            [
                {
                    "type": PydanticCustomError(
                        "strict_validation",
                        "Production configurations require a database "
                        "password in strict mode.",
                    ),
                    "loc": ("database", "password"),
                    "input": config.database.password,
                }
            ],
        )
        raise ConfigurationValidationError(error.errors())
