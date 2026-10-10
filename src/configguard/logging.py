"""Logging configuration for ConfigGuard."""

import logging


def configure_logging(verbose: bool = False) -> None:
    """Configure application logging.

    Args:
        verbose: Whether to enable debug-level logging.
    """

    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        force=True,
    )
    logging.getLogger().setLevel(level)
