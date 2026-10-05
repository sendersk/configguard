"""Pydantic models for application configuration."""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class LogLevel(StrEnum):
    """Represent supported logging levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


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


class LoggingConfig(BaseModel):
    """Represent application logging configuration."""

    level: LogLevel = LogLevel.INFO


class AppConfig(BaseModel):
    """Represent the root application configuration."""

    application: ApplicationConfig
    server: ServerConfig
    database: DatabaseConfig
    logging: LoggingConfig

    @model_validator(mode="after")
    def validate_production_configuration(self) -> "AppConfig":
        """Validate production-specific configuration rules."""

        if (
            self.application.environment == "production"
            and self.server.host in {"localhost", "127.0.0.1"}
        ):
            raise ValueError(
                "Production applications must not use localhost "
                "or 127.0.0.1 as the server host."
            )

        return self