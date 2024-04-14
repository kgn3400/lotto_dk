"""Constants for the Lotto DK integration."""

from logging import Logger, getLogger

DOMAIN = "lotto_dk"
DOMAIN_NAME = "Lotto DK"
LOGGER: Logger = getLogger(__name__)

TRANSLATION_KEY = DOMAIN
CONF_EURO_JACKPOT: str = "euro_jackpot"
CONF_LOTTO: str = "lotto"
CONF_VIKING_LOTTO: str = "viking_lotto"
