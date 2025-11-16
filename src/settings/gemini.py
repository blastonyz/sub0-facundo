from typing import Optional

from pydantic import Field, SecretStr

from src.settings.base import ProjectSettings


class _GeminiSettings(ProjectSettings):
    API_KEY: Optional[SecretStr] = Field(
        None,
        alias="GOOGLE_API_KEY",
        description="Alternate API key name for Google GenAI",
    )


GeminiSettings = _GeminiSettings()
