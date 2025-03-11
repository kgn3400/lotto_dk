"""Constants for the Lotto DK integration."""

from logging import Logger, getLogger

DOMAIN = "lotto_dk"
DOMAIN_NAME = "Lotto DK"
LOGGER: Logger = getLogger(__name__)

TRANSLATION_KEY = DOMAIN
TRANSLATION_KEY_MISSING_TIMER_ENTITY = "missing_timer_entity"

CONF_EURO_JACKPOT: str = "euro_jackpot"
CONF_LOTTO: str = "lotto"
CONF_VIKING_LOTTO: str = "viking_lotto"

CONF_RESTART_TIMER = "restart_timer"
CONF_LISTEN_TO_TIMER_TRIGGER = "listen_to_timer_trigger"
