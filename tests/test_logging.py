
"""Tests for logging configuration."""

import logging

from configguard.logging import configure_logging


def test_configure_logging_sets_info_level() -> None:
    """Verify that logging uses INFO level by default."""

    configure_logging()

    assert logging.getLogger().level == logging.INFO


def test_configure_logging_sets_debug_level() -> None:
    """Verify that verbose logging enables DEBUG level."""

    configure_logging(verbose=True)

    assert logging.getLogger().level == logging.DEBUG
