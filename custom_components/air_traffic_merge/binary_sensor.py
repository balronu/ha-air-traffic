"""Binary sensor backed by the shared Air Traffic coordinator."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import AirTrafficCoordinator
from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    async_add_entities([AirTrafficTrackedPresentBinarySensor(hass.data[DOMAIN][entry.entry_id], entry)])


class AirTrafficTrackedPresentBinarySensor(CoordinatorEntity[AirTrafficCoordinator], BinarySensorEntity):
    _attr_name = "Air Traffic Tracked Present"
    _attr_icon = "mdi:radar"

    def __init__(self, coordinator: AirTrafficCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_tracked_present"

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data and self.coordinator.data.tracked_count)

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data
        return {
            "tracking_enabled": bool(data and data.tracking_enabled),
            "matched_callsigns": data.matched_callsigns if data else [],
            "matched_registrations": data.matched_registrations if data else [],
        }
