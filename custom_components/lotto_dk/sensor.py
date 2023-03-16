"""Support for Lotto dK."""
from __future__ import annotations

from os import getcwd

from homeassistant.components.sensor import (  # SensorDeviceClass,; SensorEntityDescription,
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .entity import ComponentEntity
from .component_api import ComponentApi, LottoTypes


# ------------------------------------------------------
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Sensor setup"""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    component_api: ComponentApi = hass.data[DOMAIN][entry.entry_id]["component_api"]

    sensors = []

    # Euro jackpot
    if component_api.get_euro_jackpot:
        sensors.append(
            LottoSensor(coordinator, entry, component_api, LottoTypes.EURO_JACKPOT)
        )

    # Lotto
    if component_api.get_lotto:
        sensors.append(LottoSensor(coordinator, entry, component_api, LottoTypes.LOTTO))

    # Viking Lotto
    if component_api.get_viking_lotto:
        sensors.append(
            LottoSensor(coordinator, entry, component_api, LottoTypes.VIKING_LOTTO)
        )

    sensors.append(LottoScrollSensor(coordinator, entry, component_api))

    async_add_entities(sensors)


# ------------------------------------------------------
# ------------------------------------------------------
class LottoSensor(ComponentEntity, SensorEntity):
    """Sensor class for lotto"""

    # ------------------------------------------------------
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        component_api: ComponentApi,
        lotto_type: LottoTypes,
    ) -> None:
        super().__init__(coordinator, entry)

        self.component_api = component_api
        self.coordinator = coordinator
        self.lotto_type = lotto_type

        if self.lotto_type == LottoTypes.EURO_JACKPOT:
            self._name = "Euro jackpot"
            self._unique_id = "euro_jackpot"
        elif self.lotto_type == LottoTypes.VIKING_LOTTO:
            self._name = "Viking lotto"
            self._unique_id = "viking_lotto"
        else:
            self._name = "Lotto"
            self._unique_id = "lotto"

    # ------------------------------------------------------
    @property
    def name(self) -> str:
        return self._name

    # ------------------------------------------------------
    @property
    def icon(self) -> str:
        return "mdi:cash-multiple"

    # ------------------------------------------------------
    @property
    def native_value(self) -> str | None:
        if self.lotto_type == LottoTypes.EURO_JACKPOT:
            return (
                str(int(self.component_api.euro_jackpot_price_pool / 1000000)) + " mio"
            )
        elif self.lotto_type == LottoTypes.VIKING_LOTTO:
            return (
                str(int(self.component_api.viking_lotto_price_pool / 1000000)) + " mio"
            )
        else:
            return str(int(self.component_api.lotto_price_pool / 1000000)) + " mio"

    # ------------------------------------------------------
    @property
    def extra_state_attributes(self) -> dict:
        attr: dict = {}

        if self.lotto_type == LottoTypes.EURO_JACKPOT:
            attr["price_pool"] = self.component_api.euro_jackpot_price_pool
        elif self.lotto_type == LottoTypes.VIKING_LOTTO:
            attr["price_pool"] = self.component_api.viking_lotto_price_pool
        else:
            attr["price_pool"] = self.component_api.lotto_price_pool
        attr["dir"] = getcwd()
        return attr

    # ------------------------------------------------------
    @property
    def unique_id(self) -> str:
        return self._unique_id

    # ------------------------------------------------------
    @property
    def should_poll(self) -> bool:
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    # ------------------------------------------------------
    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    # ------------------------------------------------------
    async def async_update(self) -> None:
        """Update the entity. Only used by the generic entity update service."""
        await self.coordinator.async_request_refresh()

    # ------------------------------------------------------
    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


# ------------------------------------------------------
# ------------------------------------------------------
class LottoScrollSensor(ComponentEntity, SensorEntity):
    """Sensor class for lotto scroll"""

    # ------------------------------------------------------
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
        component_api: ComponentApi,
    ) -> None:
        super().__init__(coordinator, entry)

        self.component_api = component_api
        self.coordinator = coordinator
        self._name = "Lotto puljer"
        self._unique_id = "lotto_puljer"

    # ------------------------------------------------------
    @property
    def name(self) -> str:
        return self._name

    # ------------------------------------------------------
    @property
    def icon(self) -> str:
        return "mdi:cash-multiple"

    # ------------------------------------------------------
    # @property
    # def state(self) -> str:
    #     return self.component_api.lotto_price_pool_scroll

    # ------------------------------------------------------
    @property
    def native_value(self) -> str | None:
        return self.component_api.lotto_price_pool_scroll

    # ------------------------------------------------------
    @property
    def extra_state_attributes(self) -> dict:
        attr: dict = {}

        return attr

    # ------------------------------------------------------
    @property
    def unique_id(self) -> str:
        return self._unique_id

    # ------------------------------------------------------
    @property
    def should_poll(self) -> bool:
        """No need to poll. Coordinator notifies entity of updates."""
        return False

    # ------------------------------------------------------
    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    # ------------------------------------------------------
    async def async_update(self) -> None:
        """Update the entity. Only used by the generic entity update service."""
        await self.coordinator.async_request_refresh()

    # ------------------------------------------------------
    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
