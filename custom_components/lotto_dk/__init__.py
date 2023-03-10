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

PLATFORMS: list[Platform] = [Platform.SENSOR]


# ------------------------------------------------------------------
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Lotto DK from a config entry."""
    session = async_get_clientsession(hass)

    hass.data.setdefault(DOMAIN, {})

    if entry.options.get(CONF_EURO_JACKPOT, None) is None:
        lotto_api: LottoApi = LottoApi(
            session,
            entry.data[CONF_EURO_JACKPOT],
            entry.data[CONF_LOTTO],
            entry.data[CONF_VIKING_LOTTO],
        )
    else:
        lotto_api: LottoApi = LottoApi(
            session,
            entry.options[CONF_EURO_JACKPOT],
            entry.options[CONF_LOTTO],
            entry.options[CONF_VIKING_LOTTO],
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

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))

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


async def update_listener(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
) -> None:
    """Reload on config entry update."""

    lotto_api: LottoApi = hass.data[DOMAIN][config_entry.entry_id]["lotto_api"]
    lotto_api.get_euro_jackpot = config_entry.options[CONF_EURO_JACKPOT]
    lotto_api.get_lotto = config_entry.options[CONF_LOTTO]
    lotto_api.get_viking_lotto = config_entry.options[CONF_VIKING_LOTTO]
    await hass.config_entries.async_reload(config_entry.entry_id)

    return
