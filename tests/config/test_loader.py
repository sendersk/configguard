"""Tests for configuration loading."""

from pathlib import Path

import pytest

from configguard.config.loader import (
    ConfigurationLoadError,
    load_configuration,
)


def test_load_configuration_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """Verify that a missing configuration file is rejected."""

    path = tmp_path / "config.yaml"

    with pytest.raises(ConfigurationLoadError, match="does not exist"):
        load_configuration(path)


def test_load_configuration_reads_yaml_file(
    tmp_path: Path,
) -> None:
    """Verify that a valid YAML file is loaded."""

    path = tmp_path / "config.yaml"
    path.write_text(
        """
application:
  name: payment-api
  environment: production
""",
        encoding="utf-8",
    )

    result = load_configuration(path)

    assert result == {
        "application": {
            "name": "payment-api",
            "environment": "production",
        }
    }


def test_load_configuration_rejects_invalid_yaml(
    tmp_path: Path,
) -> None:
    """Verify that invalid YAML is rejected."""

    path = tmp_path / "config.yaml"
    path.write_text(
        """
application:
  name: payment-api
  environment: [production
""",
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigurationLoadError,
        match="Invalid YAML configuration",
    ):
        load_configuration(path)


@pytest.mark.parametrize(
    ("content", "description"),
    [
        ("- application", "a list"),
        ("configuration", "a scalar"),
    ],
)
def test_load_configuration_rejects_non_mapping_root(
    tmp_path: Path,
    content: str,
    description: str,
) -> None:
    """Verify that a non-mapping YAML root is rejected."""

    path = tmp_path / "config.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(
        ConfigurationLoadError,
        match="Configuration root must be a mapping",
    ):
        load_configuration(path)