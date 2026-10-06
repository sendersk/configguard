"""Tests for JSON validation output."""

import json

from configguard.config.result import ValidationResult
from configguard.output.json import format_json_result


def test_format_json_result_for_valid_configuration() -> None:
    """Verify that valid configurations produce valid JSON output."""

    result = ValidationResult(valid=True)

    output = format_json_result(result)

    assert json.loads(output) == {
        "valid": True,
        "errors": [],
    }


def test_format_json_result_for_invalid_configuration() -> None:
    """Verify that validation errors are serialized as JSON."""

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

    output = format_json_result(result)

    assert json.loads(output) == {
        "valid": False,
        "errors": [
            {
                "loc": ["server", "port"],
                "msg": "Input should be less than or equal to 65535",
                "type": "less_than_equal",
            }
        ],
    }


def test_format_json_result_is_pretty_printed() -> None:
    """Verify that JSON output is formatted for readability."""

    result = ValidationResult(valid=True)

    output = format_json_result(result)

    assert output == '{\n  "valid": true,\n  "errors": []\n}'