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


class DatabaseConfig(BaseModel):
    """Represent application database configuration."""

    host: str = Field(min_length=1)
    port: int = Field(default=5432, ge=1, le=65535)
    name: str = Field(min_length=1)
    username: str = Field(min_length=1)
    password: str | None = None


class AppConfig(BaseModel):
    """Represent the root application configuration."""

    application: ApplicationConfig
    server: ServerConfig
    database: DatabaseConfig