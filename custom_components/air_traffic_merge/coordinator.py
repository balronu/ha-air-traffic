"""Coordinated acquisition and merge of the configured Air Traffic sources."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from aiohttp import ClientError, ClientResponseError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import (
    CONF_ADSB_ENTITY, CONF_ADSB_SOURCE, CONF_ADSB_URL, CONF_ENABLE_TRACKING,
    CONF_FR24_ENTITY, CONF_SCAN_INTERVAL, CONF_TRACK_CALLSIGNS, CONF_TRACK_MODE,
    CONF_TRACK_REGISTRATIONS, DEFAULT_ADSB_SOURCE, DEFAULT_ENABLE_TRACKING,
    DEFAULT_SCAN_INTERVAL, DEFAULT_TRACK_MODE, DOMAIN,
)
from .data import Flight, apply_tracking, merge_sources, parse_csv, text

_LOGGER = logging.getLogger(__name__)


@dataclass
class AirTrafficSnapshot:
    flights: list[dict[str, Any]]
    aircraft: list[dict[str, Any]]
    messages: int | None
    now: int | None
    fr24_count: int
    adsb_count: int
    merged_count: int
    tracking_enabled: bool
    tracking_mode: str
    matched_callsigns: list[str]
    matched_registrations: list[str]
    last_update: float
    source_errors: dict[str, str]
    data_stale: bool

    @property
    def tracked_count(self) -> int:
        return sum(1 for flight in self.flights if flight.get("tracked"))


class AirTrafficCoordinator(DataUpdateCoordinator[AirTrafficSnapshot]):
    """Fetch configured sources and publish one normalized snapshot."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.entry = entry
        self.session = async_get_clientsession(hass)
        self._last_fr24: list[dict[str, Any]] = []
        self._last_adsb: list[dict[str, Any]] = []
        self._last_adsb_messages: int | None = None
        self._last_adsb_now: int | None = None
        self._previous_tracked: set[str] = set()
        super().__init__(
            hass, _LOGGER, name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=timedelta(seconds=self._scan_interval), always_update=True,
        )

    @property
    def _config(self) -> dict[str, Any]:
        return {**self.entry.data, **self.entry.options}

    @property
    def _scan_interval(self) -> int:
        try:
            return max(5, int(self._config.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)))
        except (TypeError, ValueError):
            return DEFAULT_SCAN_INTERVAL

    async def _async_update_data(self) -> AirTrafficSnapshot:
        config = self._config
        source_mode = config.get("source_mode", "both")
        source_errors: dict[str, str] = {}
        fr24: list[dict[str, Any]] = []
        adsb: list[dict[str, Any]] = []
        if source_mode in {"fr24_only", "both"}:
            fr24, error = await self._read_fr24(config.get(CONF_FR24_ENTITY))
            if error:
                source_errors["fr24"] = error
        if source_mode in {"adsb_only", "both"}:
            adsb, error = await self._read_adsb(config)
            if error:
                source_errors["adsb"] = error

        flights = merge_sources(fr24, adsb)
        tracking_enabled = bool(config.get(CONF_ENABLE_TRACKING, DEFAULT_ENABLE_TRACKING))
        tracking_mode = text(config.get(CONF_TRACK_MODE, DEFAULT_TRACK_MODE))
        flights, matched_callsigns, matched_registrations = apply_tracking(
            flights, tracking_enabled, tracking_mode,
            parse_csv(config.get(CONF_TRACK_CALLSIGNS)), parse_csv(config.get(CONF_TRACK_REGISTRATIONS)),
        )
        current_tracked = {flight.tracked_target for flight in flights if flight.tracked_target}
        self._fire_tracking_events(current_tracked, tracking_mode)

        return AirTrafficSnapshot(
            flights=[flight.as_dict() if isinstance(flight, Flight) else flight for flight in flights],
            aircraft=list(self._last_adsb), messages=self._last_adsb_messages, now=self._last_adsb_now,
            fr24_count=len(fr24), adsb_count=len(adsb),
            merged_count=sum(1 for flight in flights if flight.source == "BOTH"),
            tracking_enabled=tracking_enabled, tracking_mode=tracking_mode,
            matched_callsigns=matched_callsigns, matched_registrations=matched_registrations,
            last_update=dt_util.utcnow().timestamp(), source_errors=source_errors,
            data_stale=bool(source_errors),
        )

    async def _read_fr24(self, entity_id: Any) -> tuple[list[dict[str, Any]], str | None]:
        entity = self.hass.states.get(entity_id) if entity_id else None
        if entity is None:
            return (self._last_fr24, f"Entity nicht verfügbar: {entity_id}") if entity_id else ([], "Keine FR24-Entity konfiguriert")
        if getattr(entity, "state", "") in {"unknown", "unavailable"}:
            return self._last_fr24, f"Entity nicht verfügbar: {entity_id}"
        flights = entity.attributes.get("flights", []) if isinstance(entity.attributes, dict) else []
        if not isinstance(flights, list):
            return self._last_fr24, "FR24-Attribut flights ist keine Liste"
        self._last_fr24 = [item for item in flights if isinstance(item, dict)]
        return self._last_fr24, None

    async def _read_adsb(self, config: dict[str, Any]) -> tuple[list[dict[str, Any]], str | None]:
        source = config.get(CONF_ADSB_SOURCE, DEFAULT_ADSB_SOURCE)
        if source == "entity":
            entity_id = config.get(CONF_ADSB_ENTITY)
            entity = self.hass.states.get(entity_id) if entity_id else None
            if entity is None:
                return self._last_adsb, f"Entity nicht verfügbar: {entity_id or 'unbekannt'}"
            if getattr(entity, "state", "") in {"unknown", "unavailable"}:
                return self._last_adsb, f"Entity nicht verfügbar: {entity_id}"
            aircraft = entity.attributes.get("aircraft", []) if isinstance(entity.attributes, dict) else []
            if not isinstance(aircraft, list):
                return self._last_adsb, "ADS-B-Attribut aircraft ist keine Liste"
            self._last_adsb = [item for item in aircraft if isinstance(item, dict)]
            self._last_adsb_messages = entity.attributes.get("messages") if isinstance(entity.attributes, dict) else None
            self._last_adsb_now = entity.attributes.get("now") if isinstance(entity.attributes, dict) else None
            return self._last_adsb, None

        url = text(config.get(CONF_ADSB_URL))
        if not url:
            return self._last_adsb, "Keine ADS-B-URL konfiguriert"
        last_error = "ADS-B-Abfrage fehlgeschlagen"
        for attempt in range(3):
            try:
                async with asyncio.timeout(10):
                    async with self.session.get(url) as response:
                        if response.status == 429 or response.status >= 500:
                            raise ClientResponseError(
                                response.request_info, response.history,
                                status=response.status, message="retryable response",
                            )
                        response.raise_for_status()
                        payload = await response.json(content_type=None)
                aircraft = payload.get("aircraft", []) if isinstance(payload, dict) else []
                if not isinstance(aircraft, list):
                    return self._last_adsb, "ADS-B-Antwort enthält keine aircraft-Liste"
                self._last_adsb = [item for item in aircraft if isinstance(item, dict)]
                self._last_adsb_messages = payload.get("messages")
                self._last_adsb_now = payload.get("now")
                return self._last_adsb, None
            except ClientResponseError as err:
                last_error = f"ADS-B HTTP {err.status}"
                if err.status not in {429} and err.status < 500:
                    break
            except (ClientError, asyncio.TimeoutError, OSError, ValueError, TypeError) as err:
                last_error = f"ADS-B-Abfrage fehlgeschlagen: {type(err).__name__}"
            if attempt < 2:
                await asyncio.sleep(2**attempt)
        _LOGGER.debug("ADS-B source failed after retries: %s", last_error)
        return self._last_adsb, last_error

    def _fire_tracking_events(self, current: set[str], mode: str) -> None:
        appeared = sorted(current - self._previous_tracked)
        disappeared = sorted(self._previous_tracked - current)
        for target in appeared:
            self.hass.bus.async_fire(f"{DOMAIN}_tracked", {"action": "appeared", "target": target, "track_mode": mode})
        for target in disappeared:
            self.hass.bus.async_fire(f"{DOMAIN}_tracked", {"action": "disappeared", "target": target, "track_mode": mode})
        self._previous_tracked = current
