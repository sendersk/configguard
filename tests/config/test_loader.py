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


def test_load_configuration_is_not_implemented_yet(
    tmp_path: Path,
) -> None:
    """Verify that existing files reach the loader implementation."""

    path = tmp_path / "config.yaml"
    path.write_text("application: {}", encoding="utf-8")

    with pytest.raises(NotImplementedError):
        load_configuration(path)