"""Tests for validation result models."""

from configguard.config.result import ValidationResult


def test_validation_result_represents_valid_configuration() -> None:
    """Verify that a valid result can be created."""

    result = ValidationResult(valid=True)

    assert result.valid is True
    assert result.errors == []


def test_validation_result_represents_invalid_configuration() -> None:
    """Verify that an invalid result can contain errors."""

    errors = [
        {
            "loc": ("server", "port"),
            "msg": "Input should be less than or equal to 65535",
            "type": "less_than_equal",
        }
    ]

    result = ValidationResult(valid=False, errors=errors)

    assert result.valid is False
    assert result.errors == errors