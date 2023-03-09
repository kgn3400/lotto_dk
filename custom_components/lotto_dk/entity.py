"""Base entity for the Lotto DK integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN


class LottoEntity(CoordinatorEntity[DataUpdateCoordinator], Entity):
    """Defines a Lotto entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the Lotto entity."""
        super().__init__(coordinator=coordinator)
        self._attr_device_info = DeviceInfo(
            # configuration_url="https://mit.odenserenovation.dk/hentkalender",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, "Lotto DK")},
            manufacturer="KGN",
            suggested_area="Hjem",
            sw_version="1.0.1",
            name="Lotto DK",
        )
