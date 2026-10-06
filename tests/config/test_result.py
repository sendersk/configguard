"""Tests for validation result models."""

from pydantic_core import ErrorDetails

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


def test_validation_result_serializes_to_json() -> None:
    """Verify that a validation result can be serialized to JSON."""

    result = ValidationResult(
        valid=False,
        errors=[
            {
                "loc": ("server", "port"),
                "msg": "Input should be less than or equal to 65535",
                "type": "less_than_equal",
            }
        ],
    )

    data = result.model_dump(mode="json")

    assert data == {
        "valid": False,
        "errors": [
            {
                "loc": ["server", "port"],
                "msg": "Input should be less than or equal to 65535",
                "type": "less_than_equal",
            }
        ],
    }


def test_validation_result_uses_independent_error_lists() -> None:
    """Verify that validation results do not share error lists."""

    first = ValidationResult(valid=True)
    second = ValidationResult(valid=True)

    first.errors.append({"msg": "example"})

    assert first.errors == [{"msg": "example"}]
    assert second.errors == []


def test_validation_result_can_be_created_from_errors() -> None:
    """Verify that validation errors can be converted to a result."""

    errors: list[ErrorDetails] = [
        {
            "type": "less_than_equal",
            "loc": ("server", "port"),
            "msg": "Input should be less than or equal to 65535",
            "input": 70000,
            "ctx": {"le": 65535},
        }
    ]

    result = ValidationResult.from_errors(errors)

    assert result.valid is False
    assert len(result.errors) == 1
    assert result.errors[0]["type"] == "less_than_equal"
    assert result.errors[0]["loc"] == ("server", "port")


def test_validation_result_copies_error_data() -> None:
    """Verify that validation results contain independent error data."""

    errors: list[ErrorDetails] = [
        {
            "type": "value_error",
            "loc": ("application",),
            "msg": "Invalid configuration",
            "input": {},
        }
    ]

    result = ValidationResult.from_errors(errors)

    result.errors[0]["msg"] = "Changed"

    assert errors[0]["msg"] == "Invalid configuration"