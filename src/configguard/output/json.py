"""JSON validation output."""

import json

from configguard.config.result import ValidationResult


def format_json_result(result: ValidationResult) -> str:
    """Format a validation result as JSON.

    Args:
        result: Configuration validation result.

    Returns:
        JSON representation of the validation result.
    """

    return json.dumps(
        result.model_dump(mode="json"),
        indent=2,
    )