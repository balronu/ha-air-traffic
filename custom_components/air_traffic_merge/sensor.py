"""Sensors backed by the shared Air Traffic coordinator."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import AirTrafficCoordinator
from .const import DOMAIN


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    coordinator: AirTrafficCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        AirTrafficMergedSensor(coordinator, entry),
        AirTrafficTrackedCountSensor(coordinator, entry),
    ])


class AirTrafficMergedSensor(CoordinatorEntity[AirTrafficCoordinator], SensorEntity):
    _attr_name = "Air Traffic Merged"
    _attr_icon = "mdi:airplane"

    def __init__(self, coordinator: AirTrafficCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_merged"

    @property
    def native_value(self) -> int:
        return len(self.coordinator.data.flights) if self.coordinator.data else 0

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data
        if data is None:
            return {}
        return {
            "last_update": int(data.last_update),
            "flights": data.flights,
            "aircraft": data.aircraft,
            "messages": data.messages,
            "now": data.now,
            "fr24_count": data.fr24_count,
            "adsb_count": data.adsb_count,
            "merged_count": data.merged_count,
            "tracking_enabled": data.tracking_enabled,
            "tracked_active_count": data.tracked_count,
            "matched_callsigns": data.matched_callsigns,
            "matched_registrations": data.matched_registrations,
            "source_errors": data.source_errors,
            "data_stale": data.data_stale,
        }


class AirTrafficTrackedCountSensor(CoordinatorEntity[AirTrafficCoordinator], SensorEntity):
    _attr_name = "Air Traffic Tracked Count"
    _attr_icon = "mdi:radar"

    def __init__(self, coordinator: AirTrafficCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_tracked_count"

    @property
    def native_value(self) -> int:
        return self.coordinator.data.tracked_count if self.coordinator.data else 0

    @property
    def extra_state_attributes(self) -> dict:
        data = self.coordinator.data
        if data is None:
            return {}
        return {
            "tracking_enabled": data.tracking_enabled,
            "mode": data.tracking_mode,
            "matched_callsigns": data.matched_callsigns,
            "matched_registrations": data.matched_registrations,
            "matched_aircraft": [flight for flight in data.flights if flight.get("tracked")],
        }
