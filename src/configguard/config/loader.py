"""Configuration loading utilities."""

from pathlib import Path
from typing import Any


class ConfigurationLoadError(Exception):
    """Raised when a configuration file cannot be loaded."""


def load_configuration(path: Path) -> dict[str, Any]:
    """Load configuration data from a file.

    Args:
        path: Path to the configuration file.

    Returns:
        Configuration data as a dictionary.

    Raises:
        ConfigurationLoadError: If the configuration cannot be loaded.
    """

    if not path.is_file():
        raise ConfigurationLoadError(
            f"Configuration file does not exist: {path}"
        )

    raise NotImplementedError