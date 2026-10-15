"""Pure Air Traffic source normalization and merge helpers."""

from __future__ import annotations

from dataclasses import dataclass, asdict
import math
from typing import Any


def text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def number(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def feet_to_m(value: Any) -> float | None:
    result = number(value)
    return round(result * 0.3048) if result is not None else None


def knots_to_kmh(value: Any) -> float | None:
    result = number(value)
    return round(result * 1.852) if result is not None else None


def normalize(value: Any) -> str:
    return text(value).upper()


def parse_csv(value: Any) -> list[str]:
    return list(dict.fromkeys(normalize(part) for part in text(value).split(",") if text(part)))


def _first(record: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        value = record.get(key)
        if value is not None and value != "":
            return value
    return None


def _identity(record: dict[str, Any], source: str) -> str:
    hex_code = normalize(_first(record, "hex", "icao", "icao24"))
    registration = normalize(_first(record, "registration", "r", "aircraft_registration"))
    callsign = normalize(_first(record, "callsign", "flight", "flight_number"))
    if registration:
        return f"reg:{registration}"
    if hex_code:
        return f"hex:{hex_code}"
    if callsign:
        return f"callsign:{callsign}"
    return f"{source.lower()}:anonymous:{id(record)}"


def normalize_adsb(record: dict[str, Any]) -> dict[str, Any]:
    seen_seconds = number(record.get("seen_pos", record.get("seen")))
    position_stale = seen_seconds is not None and seen_seconds > 300
    return {
        "registration": text(_first(record, "r", "registration")),
        "hex": text(_first(record, "hex", "icao24")),
        "callsign": text(_first(record, "flight", "callsign")),
        "aircraft_model": text(_first(record, "t", "aircraft_model")),
        "airline": text(record.get("airline")),
        "alt_m": feet_to_m(_first(record, "alt_baro", "altitude")),
        "spd_kmh": knots_to_kmh(_first(record, "gs", "speed")),
        "dist_km": number(_first(record, "r_dst", "distance")),
        "dir_deg": number(_first(record, "r_dir", "track", "heading")),
        "latitude": valid_latitude(_first(record, "lat", "latitude")),
        "longitude": valid_longitude(_first(record, "lon", "longitude")),
        "position_age_s": seen_seconds,
        "position_stale": position_stale,
        "category": text(record.get("category")),
        "squawk": text(record.get("squawk")),
        "source": "ADSB",
        "_identity": _identity(record, "ADSB"),
    }


def normalize_fr24(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "registration": text(_first(record, "aircraft_registration", "registration", "r")),
        "hex": text(_first(record, "hex", "icao24")),
        "callsign": text(_first(record, "flight_number", "callsign", "flight")),
        "aircraft_model": text(_first(record, "aircraft_model", "aircraft_type", "type")),
        "airline": text(_first(record, "airline_short", "airline")),
        "alt_m": number(_first(record, "alt_m", "altitude")),
        "spd_kmh": number(_first(record, "spd_kmh", "speed")),
        "dist_km": number(_first(record, "dist_km", "distance")),
        "dir_deg": number(_first(record, "dir_deg", "heading", "track")),
        "latitude": valid_latitude(_first(record, "latitude", "lat")),
        "longitude": valid_longitude(_first(record, "longitude", "lon")),
        "position_age_s": number(record.get("position_age_s")),
        "position_stale": bool(record.get("position_stale", False)),
        "category": text(record.get("category")),
        "squawk": text(record.get("squawk")),
        "source": "FR24",
        "_identity": _identity(record, "FR24"),
    }


@dataclass
class Flight:
    key: str
    registration: str = ""
    hex: str = ""
    callsign: str = ""
    source: str = ""
    aircraft_model: str = ""
    airline: str = ""
    alt_m: float | None = None
    spd_kmh: float | None = None
    dist_km: float | None = None
    dir_deg: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    position_age_s: float | None = None
    position_stale: bool = False
    category: str = ""
    squawk: str = ""
    tracked: bool = False
    tracked_by: str = ""
    tracked_target: str = ""

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["source_text"] = self.source
        return result


def _merge_value(left: Any, right: Any) -> Any:
    if right is not None and right != "":
        return right
    return left


def valid_latitude(value: Any) -> float | None:
    result = number(value)
    return result if result is not None and -90 <= result <= 90 else None


def valid_longitude(value: Any) -> float | None:
    result = number(value)
    return result if result is not None and -180 <= result <= 180 else None


def merge_sources(fr24: list[dict[str, Any]], adsb: list[dict[str, Any]]) -> list[Flight]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for source, records in (("FR24", fr24), ("ADSB", adsb)):
        for record in records:
            if not isinstance(record, dict):
                continue
            normalized = normalize_fr24(record) if source == "FR24" else normalize_adsb(record)
            grouped.setdefault(normalized.pop("_identity"), []).append(normalized)

    flights: list[Flight] = []
    for key, records in grouped.items():
        merged: dict[str, Any] = {}
        sources: set[str] = set()
        for record in records:
            sources.add(record["source"])
            for field, value in record.items():
                if field != "source" and value is not None and value != "":
                    merged[field] = _merge_value(merged.get(field), value)
        source = "BOTH" if len(sources) > 1 else next(iter(sources))
        flights.append(Flight(key=key, source=source, **merged))

    flights.sort(key=lambda flight: (not flight.tracked, {"BOTH": 0, "ADSB": 1, "FR24": 2}.get(flight.source, 9), flight.dist_km if flight.dist_km is not None else 999999, flight.registration or flight.hex or flight.callsign or flight.key))
    return flights


def apply_tracking(flights: list[Flight], enabled: bool, mode: str, callsigns: list[str], registrations: list[str]) -> tuple[list[Flight], list[str], list[str]]:
    mode = mode if mode in {"callsign", "registration", "both"} else "callsign"
    wanted_callsigns = set(callsigns)
    wanted_registrations = set(registrations)
    matched_callsigns: set[str] = set()
    matched_registrations: set[str] = set()
    for flight in flights:
        callsign = normalize(flight.callsign)
        registration = normalize(flight.registration)
        callsign_hit = enabled and callsign in wanted_callsigns and bool(callsign)
        registration_hit = enabled and registration in wanted_registrations and bool(registration)
        flight.tracked = (mode in {"callsign", "both"} and callsign_hit) or (mode in {"registration", "both"} and registration_hit)
        if flight.tracked:
            if registration_hit and mode in {"registration", "both"}:
                flight.tracked_by, flight.tracked_target = "registration", registration
                matched_registrations.add(registration)
            else:
                flight.tracked_by, flight.tracked_target = "callsign", callsign
                matched_callsigns.add(callsign)
        else:
            flight.tracked_by = flight.tracked_target = ""
    return flights, sorted(matched_callsigns), sorted(matched_registrations)
