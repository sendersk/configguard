"""Pydantic models for application configuration."""

from typing import Literal

from pydantic import BaseModel, Field


class ApplicationConfig(BaseModel):
    """Represent basic application configuration."""

    name: str = Field(min_length=1)
    environment: Literal["development", "testing", "staging", "production"]


class ServerConfig(BaseModel):
    """Represent application server configuration."""

    host: str = Field(min_length=1)
    port: int = Field(ge=1, le=65535)


class AppConfig(BaseModel):
    """Represent the root application configuration."""

    application: ApplicationConfig
    server: ServerConfig