"""Configuration loading utilities."""

from pathlib import Path
from typing import Any

import yaml


class ConfigurationLoadError(Exception):
    """Raised when a configuration file cannot be loaded."""


def load_configuration(path: Path) -> dict[str, Any]:
    """Load configuration data from a YAML file.

    Args:
        path: Path to the YAML configuration file.

    Returns:
        Configuration data as a dictionary.

    Raises:
        ConfigurationLoadError: If the configuration cannot be loaded.
    """

    if not path.is_file():
        raise ConfigurationLoadError(
            f"Configuration file does not exist: {path}"
        )

    try:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as error:
        raise ConfigurationLoadError(
            f"Invalid YAML configuration: {path}"
        ) from error

    if not isinstance(data, dict):
        raise ConfigurationLoadError(
            f"Configuration root must be a mapping: {path}"
        )

    return data