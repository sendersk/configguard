
"""Tests for logging configuration."""

import logging

import pytest

from configguard.logging import configure_logging


@pytest.fixture
def reset_root_logger() -> None:
    """Restore the root logger state after a test."""

    root_logger = logging.getLogger()
    original_level = root_logger.level
    original_handlers = root_logger.handlers.copy()

    yield

    root_logger.setLevel(original_level)

    for handler in root_logger.handlers.copy():
        if handler not in original_handlers:
            root_logger.removeHandler(handler)
            handler.close()


def test_configure_logging_sets_info_level(
    reset_root_logger: None,
) -> None:
    """Verify that logging uses INFO level by default."""

    configure_logging()

    assert logging.getLogger().level == logging.INFO


def test_configure_logging_sets_debug_level(
    reset_root_logger: None,
) -> None:
    """Verify that verbose logging enables DEBUG level."""

    configure_logging(verbose=True)

    assert logging.getLogger().level == logging.DEBUG
