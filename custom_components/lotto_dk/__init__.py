"""The Lotto DK integration."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_EURO_JACKPOT, CONF_LOTTO, CONF_VIKING_LOTTO, DOMAIN, LOGGER
from .lotto_api import LottoApi

# DODO List the platforms that you want to support.
# For your initial PR, limit it to 1 platform.
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Lotto DK from a config entry."""
    session = async_get_clientsession(hass)

    # if hass.data.get(DOMAIN) is None:
    hass.data.setdefault(DOMAIN, {})

    lotto_api: LottoApi = LottoApi(
        session,
        entry.data[CONF_EURO_JACKPOT],
        entry.data[CONF_LOTTO],
        entry.data[CONF_VIKING_LOTTO],
    )

    coordinator: DataUpdateCoordinator = DataUpdateCoordinator(
        hass,
        LOGGER,
        name=DOMAIN,
        update_interval=timedelta(minutes=1),
        update_method=lotto_api.update,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinator,
        "lotto_api": lotto_api,
    }

    # DODO 1. Create API instance
    # DODO 2. Validate the API connection (and authentication)
    # DODO 3. Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
