from pydantic import Field

from src.settings.base import ProjectSettings


class _DatabaseSettings(ProjectSettings):
    """Pydantic settings for PostgreSQL connection.

    The DSN can be overridden via the environment variable `DATABASE_URL`.
    By default it uses the provided Neon/Postgres connection string.
    """

    DIALECT: str = Field(
        ...,
        alias="DATABASE_DIALECT",
        description="Postgres DSN (can be overridden with env DATABASE_URL)",
        examples=["postgresql+asyncpg"],
    )
    USERNAME: str = Field(..., alias="DATABASE_USERNAME", description="Database username")
    PASSWORD: str = Field(..., alias="DATABASE_PASSWORD", description="Database password")
    HOST: str = Field(..., alias="DATABASE_HOST", description="Database host")
    PORT: int = Field(..., alias="DATABASE_PORT", description="Database port")
    DB_NAME: str = Field(..., alias="DATABASE_DB_NAME", description="Database name")

    @property
    def get_url(self) -> str:
        return f"{self.DIALECT}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB_NAME}"

DatabaseSettings = _DatabaseSettings()
