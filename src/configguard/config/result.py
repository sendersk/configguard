"""Configuration validation result models."""

from typing import Any

from pydantic import BaseModel, Field
from pydantic_core import ErrorDetails


class ValidationResult(BaseModel):
    """Represent the result of configuration validation."""

    valid: bool
    errors: list[dict[str, Any]] = Field(default_factory=list)

    @classmethod
    def from_errors(cls, errors: list[ErrorDetails]) -> "ValidationResult":
        """Create an invalid result from validation errors.

        Args:
            errors: Structured validation errors.

        Returns:
            An invalid validation result.
        """

        return cls(
            valid=False,
            errors=[dict(error) for error in errors],
        )