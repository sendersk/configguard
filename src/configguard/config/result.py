"""Configuration validation result models."""

from typing import Any

from pydantic import BaseModel, Field


class ValidationResult(BaseModel):
    """Represent the result of configuration validation."""

    valid: bool
    errors: list[dict[str, Any]] = Field(default_factory=list)