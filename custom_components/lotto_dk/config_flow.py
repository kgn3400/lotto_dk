"""Config flow for Lotto DK integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

#  from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

from .const import CONF_EURO_JACKPOT, CONF_LOTTO, CONF_VIKING_LOTTO, DOMAIN

_LOGGER = logging.getLogger(__name__)


# ------------------------------------------------------------------
async def _validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""

    if (
        data[CONF_EURO_JACKPOT] is False
        and data[CONF_LOTTO] is False
        and data[CONF_VIKING_LOTTO] is False
    ):
        raise MissingSelection

    # Return info that you want to store in the config entry.
    return {"title": "Lotto"}


# ------------------------------------------------------------------
def _create_form(
    user_input: dict[str, Any] | None = None,
) -> vol.Schema:
    """Create a form for step/option."""

    if user_input is None:
        user_input = {}

    return vol.Schema(
        {
            vol.Required(
                CONF_EURO_JACKPOT,
                default=user_input.get(CONF_EURO_JACKPOT, True),
            ): cv.boolean,
            vol.Required(
                CONF_LOTTO, default=user_input.get(CONF_LOTTO, True)
            ): cv.boolean,
            vol.Required(
                CONF_VIKING_LOTTO,
                default=user_input.get(CONF_VIKING_LOTTO, True),
            ): cv.boolean,
        }
    )


# ------------------------------------------------------------------
# ------------------------------------------------------------------
class LottoConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Lotto DK."""

    VERSION = 1

    # ------------------------------------------------------------------
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        await self.async_set_unique_id("device_unique_id_lotto_dk")
        self._abort_if_unique_id_configured()

        if user_input is not None:
            try:
                await _validate_input(self.hass, user_input)
            except MissingSelection:
                errors["base"] = "missing_selection"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="Lotto DK", data=user_input, options=user_input
                )
        else:
            user_input = {}

        return self.async_show_form(
            step_id="user",
            data_schema=_create_form(user_input),
            errors=errors,
        )

    # ------------------------------------------------------------------
    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """Get the options flow."""
        return OptionsFlowHandler(config_entry)


# ------------------------------------------------------------------
# ------------------------------------------------------------------
class OptionsFlowHandler(OptionsFlow):
    """Options flow for Lotto DK."""

    def __init__(
        self,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize options flow."""

        self.config_entry = config_entry

        self._selection: dict[str, Any] = {}
        self._configs: dict[str, Any] = self.config_entry.data.copy()
        self._options: dict[str, Any] = self.config_entry.options.copy()

    # ------------------------------------------------------------------
    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await _validate_input(self.hass, user_input)
            except MissingSelection:
                errors["base"] = "missing_selection"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title="", data=user_input)
        else:
            user_input = self._options.copy()
            # if self._options.get(CONF_EURO_JACKPOT, None) is None:
            #     user_input = self._configs.copy()
            # else:

        return self.async_show_form(
            step_id="init",
            data_schema=_create_form(user_input),
            errors=errors,
        )


# ------------------------------------------------------------------
# ------------------------------------------------------------------
class MissingSelection(HomeAssistantError):
    """Error to indicate nothing was selected."""
