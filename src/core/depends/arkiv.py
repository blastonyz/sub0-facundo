from loguru import logger
from web3 import HTTPProvider

from arkiv import Arkiv
from arkiv.account import NamedAccount
from src.settings.arkiv import ArkivSettings


def get_arkiv_client() -> Arkiv:
    """Create and return an Arkiv client instance."""
    provider = HTTPProvider(ArkivSettings.HTTP_PROVIDER)
    account = NamedAccount.from_private_key(
        ArkivSettings.PRIVATE_NAME, ArkivSettings.PRIVATE_KEY.get_secret_value()
    )
    client = Arkiv(provider, account=account)
    logger.info("Connecting to: {}", client.is_connected())
    logger.info("Account: {}", client.eth.default_account)
    return client
