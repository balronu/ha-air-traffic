# Air Traffic

Home Assistant integration for combining a configured Flightradar24 sensor
with local ADS-B data from `readsb`, `tar1090`, `adsb.im`, or another sensor
that exposes an `aircraft` attribute. The Lovelace card is included in the
integration bundle.

> This Phase 2 candidate is developed locally on `work/air-traffic-modernization`.
> The target repository `ha-air-traffic` has not been created yet.

## Features

- FR24-only, ADS-B-only, and combined source modes
- ADS-B by URL or existing Home Assistant sensor
- Registration/callsign deduplication when a stable identity is available
- Tracking by callsign, registration, or both
- Shared `DataUpdateCoordinator` for polling, refresh, unload, and error state
- Built-in `custom:air-traffic-card` Lovelace card
- Compatibility alias `custom:air-traffic-merge-card`
- Versioned, automatically registered frontend bundle

## Installation

Install the integration through HACS as an **Integration** once the future
`balronu/ha-air-traffic` repository is published. This local candidate is not
published and must not be installed into a productive Home Assistant instance.

## Existing technical identifiers

The internal Home Assistant domain remains `air_traffic_merge` for compatibility.
Existing entity IDs, config-entry IDs, unique IDs, options, and the event
`air_traffic_merge_tracked` are intentionally retained. A future domain
migration requires a separate tested import strategy.

The existing entities remain:

- `sensor.air_traffic_merged`
- `sensor.air_traffic_tracked_count`
- `binary_sensor.air_traffic_tracked_present`

## Lovelace card

```yaml
type: custom:air-traffic-card
entity: sensor.air_traffic_merged
title: Air Traffic
show_status: true
max_items: 50
```

Existing dashboards using this legacy type continue to work:

```yaml
type: custom:air-traffic-merge-card
entity: sensor.air_traffic_merged
```

The integration registers one versioned module URL:

```text
/air_traffic_merge/air-traffic-card.js?v=1.4.0-beta.1
```

It does not edit `.storage/lovelace.resources` and does not require a second
card repository. Static serving and `add_extra_js_url` registration are guarded
so repeated integration setup does not add duplicate resources.

## Data-source limitations

The integration does not call a Flightradar24 API. FR24 data must already be
available through the selected Home Assistant sensor with a `flights` list.
ADS-B URL mode expects a JSON response with an `aircraft` list. Missing fields
remain missing; the integration does not invent aircraft, coordinates, routes,
status, or airport data.

## Development checks

```text
PYTHONPATH=custom_components/air_traffic_merge python3 -m unittest discover -s tests -v
cd frontend && npm ci && npm test && npm run build
```

The build output is written to
`custom_components/air_traffic_merge/frontend/air-traffic-card.js`.
