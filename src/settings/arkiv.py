from pydantic import Field, SecretStr

from src.settings.base import ProjectSettings


class _ArkivSettings(ProjectSettings):
    HTTP_PROVIDER: str = Field(
        ...,
        alias="ARKIV_HTTP_PROVIDER",
        description="URL del proveedor HTTP para conectarse a la red Arkiv",
    )
    PRIVATE_KEY: SecretStr = Field(
        ...,
        alias="ARKIV_PRIVATE_KEY",
        description="Clave privada para la cuenta de Arkiv",
    )
    PRIVATE_NAME: str = Field(
        ...,
        alias="ARKIV_PRIVATE_NAME",
        description="Nombre privado para la cuenta de Arkiv",
    )


ArkivSettings = _ArkivSettings()