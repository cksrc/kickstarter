import os
from functools import lru_cache

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseModel):
    """API server configuration."""

    host: str = Field(default="0.0.0.0", description="API host")
    port: int = Field(default=8002, description="API port")
    debug: bool = Field(default=True, description="Debug mode")


class ProjectSettings(BaseSettings):
    """Central configuration file for Project."""

    model_config = SettingsConfigDict(
        env_file=os.getenv(
            "ENV",
            os.path.join(os.path.dirname(__file__), "../environments/.env.dev"),
        ),
        env_nested_delimiter="__",  # Allows API__HOST=localhost in env files
    )

    # Nested configuration objects
    api: ApiSettings = Field(default_factory=ApiSettings)


@lru_cache
def get_settings():
    return ProjectSettings()
