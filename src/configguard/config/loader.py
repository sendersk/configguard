"""Configuration loading utilities."""

import json
from pathlib import Path
from typing import Any

import yaml


class ConfigurationLoadError(Exception):
    """Raised when a configuration file cannot be loaded."""


def load_configuration(path: Path) -> dict[str, Any]:
    """Load configuration data from a YAML or JSON file.

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

    suffix = path.suffix.lower()

    if suffix in {".yaml", ".yml"}:
        return _load_yaml(path)

    if suffix == ".json":
        return _load_json(path)

    raise ConfigurationLoadError(
        f"Unsupported configuration format: {path.suffix}"
    )


def _load_yaml(path: Path) -> dict[str, Any]:
    """Load configuration data from a YAML file.

    Args:
        path: Path to the YAML file.

    Returns:
        Configuration data as a dictionary.

    Raises:
        ConfigurationLoadError: If the YAML cannot be parsed.
    """

    try:
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as error:
        raise ConfigurationLoadError(
            f"Invalid YAML configuration: {path}"
        ) from error

    return _validate_mapping_root(data, path)


def _load_json(path: Path) -> dict[str, Any]:
    """Load configuration data from a JSON file.

    Args:
        path: Path to the JSON file.

    Returns:
        Configuration data as a dictionary.

    Raises:
        ConfigurationLoadError: If the JSON cannot be parsed.
    """

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ConfigurationLoadError(
            f"Invalid JSON configuration: {path}"
        ) from error

    return _validate_mapping_root(data, path)


def _validate_mapping_root(
    data: Any,
    path: Path,
) -> dict[str, Any]:
    """Validate that configuration data has a mapping root.

    Args:
        data: Parsed configuration data.
        path: Path to the configuration file.

    Returns:
        Configuration data as a dictionary.

    Raises:
        ConfigurationLoadError: If the root is not a mapping.
    """

    if not isinstance(data, dict):
        raise ConfigurationLoadError(
            f"Configuration root must be a mapping: {path}"
        )

    return data