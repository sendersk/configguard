"""Human-readable validation output."""

from configguard.config.result import ValidationResult


def format_human_result(result: ValidationResult) -> str:
    """Format a validation result for human-readable output.

    Args:
        result: Configuration validation result.

    Returns:
        Formatted validation result.
    """

    if result.valid:
        return "Configuration is valid."

    lines = [
        "Configuration is invalid.",
        "",
        "Errors:",
    ]

    for error in result.errors:
        location = ".".join(str(part) for part in error["loc"])
        message = str(error["msg"])
        lines.append(f"- {location}: {message}")

    return "\n".join(lines)