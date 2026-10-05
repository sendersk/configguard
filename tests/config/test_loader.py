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
    "content",
    [
        "- application",
        "configuration",
    ],
)
def test_load_configuration_rejects_non_mapping_root(
    tmp_path: Path,
    content: str,
) -> None:
    """Verify that a non-mapping YAML root is rejected."""

    path = tmp_path / "config.yaml"
    path.write_text(content, encoding="utf-8")

    with pytest.raises(
        ConfigurationLoadError,
        match="Configuration root must be a mapping",
    ):
        load_configuration(path)


def test_load_configuration_reads_json_file(
    tmp_path: Path,
) -> None:
    """Verify that a valid JSON file is loaded."""

    path = tmp_path / "config.json"
    path.write_text(
        """
{
    "application": {
        "name": "payment-api",
        "environment": "production"
    }
}
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


def test_load_configuration_reads_yaml_file_with_yml_extension(
    tmp_path: Path,
) -> None:
    """Verify that a YAML file with a .yml extension is loaded."""

    path = tmp_path / "config.yml"
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


def test_load_configuration_rejects_invalid_json(
    tmp_path: Path,
) -> None:
    """Verify that invalid JSON is rejected."""

    path = tmp_path / "config.json"
    path.write_text(
        """
{
    "application": {
        "name": "payment-api",
        "environment": "production"
    }
""",
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigurationLoadError,
        match="Invalid JSON configuration",
    ):
        load_configuration(path)


def test_load_configuration_rejects_unsupported_format(
    tmp_path: Path,
) -> None:
    """Verify that unsupported configuration formats are rejected."""

    path = tmp_path / "config.toml"
    path.write_text(
        """
[application]
name = "payment-api"
environment = "production"
""",
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigurationLoadError,
        match="Unsupported configuration format",
    ):
        load_configuration(path)


def test_load_configuration_accepts_uppercase_json_extension(
    tmp_path: Path,
) -> None:
    """Verify that uppercase JSON extensions are accepted."""

    path = tmp_path / "config.JSON"
    path.write_text(
        """
{
    "application": {
        "name": "payment-api",
        "environment": "production"
    }
}
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


def test_load_configuration_accepts_uppercase_yaml_extension(
    tmp_path: Path,
) -> None:
    """Verify that uppercase YAML extensions are accepted."""

    path = tmp_path / "config.YAML"
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


def test_load_configuration_rejects_empty_json_file(
    tmp_path: Path,
) -> None:
    """Verify that an empty JSON file is rejected."""

    path = tmp_path / "config.json"
    path.write_text("", encoding="utf-8")

    with pytest.raises(
        ConfigurationLoadError,
        match="Invalid JSON configuration",
    ):
        load_configuration(path)


def test_load_configuration_rejects_json_list_root(
    tmp_path: Path,
) -> None:
    """Verify that a JSON list root is rejected."""

    path = tmp_path / "config.json"
    path.write_text(
        """
[
    "application"
]
""",
        encoding="utf-8",
    )

    with pytest.raises(
        ConfigurationLoadError,
        match="Configuration root must be a mapping",
    ):
        load_configuration(path)


def test_load_configuration_rejects_json_scalar_root(
    tmp_path: Path,
) -> None:
    """Verify that a JSON scalar root is rejected."""

    path = tmp_path / "config.json"
    path.write_text('"configuration"', encoding="utf-8")

    with pytest.raises(
        ConfigurationLoadError,
        match="Configuration root must be a mapping",
    ):
        load_configuration(path)