"""Tests for human-readable validation output."""

from configguard.config.result import ValidationResult
from configguard.output.human import format_human_result


def test_format_human_result_for_valid_configuration() -> None:
    """Verify that valid configurations produce a success message."""

    result = ValidationResult(valid=True)

    output = format_human_result(result)

    assert output == "Configuration is valid."


def test_format_human_result_for_invalid_configuration() -> None:
    """Verify that validation errors are formatted for humans."""

    result = ValidationResult(
        valid=False,
        errors=[
            {
                "loc": ("server", "port"),
                "msg": "Input should be less than or equal to 65535",
                "type": "less_than_equal",
            },
            {
                "loc": ("application", "environment"),
                "msg": "Invalid environment",
                "type": "value_error",
            },
        ],
    )

    output = format_human_result(result)

    assert output == (
        "Configuration is invalid.\n"
        "\n"
        "Errors:\n"
        "- server.port: Input should be less than or equal to 65535\n"
        "- application.environment: Invalid environment"
    )