<p align="center">
  <img src="images/branding/air-traffic-logo.png" alt="Air Traffic logo" width="160">
</p>

<p align="center">
  <img src="images/branding/air-traffic-readme-banner.png" alt="Air Traffic – Home Assistant integration with built-in Lovelace card">
</p>

<p align="center"><a href="README.md">🇩🇪 Deutsch</a> | 🇬🇧 <strong>English</strong></p>

# Air Traffic

Air Traffic is a Home Assistant custom integration for combining a
Flightradar24 sensor with local ADS-B data. It normalizes both inputs,
suppresses duplicates, exposes stable Home Assistant entities, and serves a
responsive Lovelace card from the same integration.

> **Release status:** Stable `v1.3.1` is the latest published release.
> `1.4.0-beta.1` is prepared but not published. The isolated Lovelace browser
> validation is still open; this README does not present the unreleased beta as
> generally available.

## Contents

- [Features](#features)
- [Supported sources](#supported-sources)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Entities and attributes](#entities-and-attributes)
- [Lovelace card](#lovelace-card)
- [Migration](#migration)
- [Updating](#updating)
- [Troubleshooting](#troubleshooting)
- [Privacy and limitations](#privacy-and-limitations)
- [Contributing](#contributing)
- [License](#license)

## Features

- FR24-only, ADS-B-only, or combined source mode
- ADS-B from a URL returning `aircraft.json`
- ADS-B from an existing Home Assistant sensor with an `aircraft` attribute
- Normalization, duplicate suppression, and source merging
- Optional tracking by callsign, registration, or both
- One shared `DataUpdateCoordinator` with retry/backoff for ADS-B URLs
- Invalid coordinates and stale ADS-B positions are represented safely
- Built-in responsive card with empty, error, unavailable, and stale states
- Aircraft selection and a detail view
- New and legacy Lovelace custom-element names in one bundle

## Supported sources

| Source | Required data | Notes |
|---|---|---|
| Flightradar24 entity | Sensor attribute `flights` containing a list | Air Traffic does not call the FR24 API or handle FR24 credentials. |
| ADS-B URL | JSON object with an `aircraft` list | Host URLs are normalized to `/data/aircraft.json`; HTTP failures and timeouts are retried. |
| ADS-B entity | Sensor attribute `aircraft` containing a list | Optional `messages` and `now` attributes are retained. |

The integration accepts common FR24/readsb/tar1090 field names and normalizes
callsign, registration, ICAO/hex, altitude, speed, heading, coordinates,
distance, category, squawk, and position age where supplied. Missing values are
left empty; they are not inferred.

## Requirements

- Home Assistant with custom integrations enabled
- HACS, or permission to install a custom component manually
- At least one supported source
- Network access from Home Assistant to the ADS-B URL in URL mode

The published stable release should be used for normal installations. The
`main` branch and `1.4.0-beta.1` are development candidates until the beta
validation gates are complete.

## Installation

### HACS

1. Open **HACS → Integrations**.
2. Search for **Air Traffic** or add the repository
   [`balronu/ha-air-traffic`](https://github.com/balronu/ha-air-traffic) as a
   custom repository of type **Integration**.
3. Install the latest published release.
4. Restart Home Assistant.
5. Add **Air Traffic** under **Settings → Devices & services → Add integration**.

The public repository was renamed from `air-traffic-merge` to `ha-air-traffic`.
The technical Home Assistant domain and integration directory intentionally
remain `air_traffic_merge` for compatibility. An existing installation should
be updated, not deleted and recreated solely because the repository name
changed.

### Manual installation

Copy `custom_components/air_traffic_merge` into
`/config/custom_components/air_traffic_merge/` and restart Home Assistant.
Manual installation is useful for development, but HACS is recommended for
published releases.

## Configuration

Open **Settings → Devices & services → Add integration**, select **Air Traffic**,
and choose a source mode:

| Flow step | Available settings |
|---|---|
| Source | FR24 only, ADS-B only, or both; tracking enabled/disabled |
| FR24 sensor | A sensor entity whose attributes contain `flights` |
| ADS-B source | URL (`aircraft.json`) or an existing sensor entity |
| ADS-B URL | URL; a host URL receives the `/data/aircraft.json` suffix |
| ADS-B entity | A sensor entity whose attributes contain `aircraft` |
| Tracking mode | Callsign, registration, or both |
| Tracking values | Comma-separated callsigns and/or registrations |

For ADS-B sources, the polling interval is clamped to a minimum of five
seconds. The default is ten seconds. The Options flow lets you change the
interval and enable/disable tracking; when tracking is enabled it also exposes
the tracking mode and values.

## Entities and attributes

Entity IDs are normally generated from the entity names. Existing IDs and
unique IDs are part of the compatibility contract and must not be renamed.

| Entity | Purpose |
|---|---|
| `sensor.air_traffic_merged` | Number of merged aircraft and the complete normalized snapshot |
| `sensor.air_traffic_tracked_count` | Number of currently tracked aircraft |
| `binary_sensor.air_traffic_tracked_present` | On while at least one tracked aircraft is present |

The merged sensor exposes these attributes:

`last_update`, `flights`, `aircraft`, `messages`, `now`, `fr24_count`,
`adsb_count`, `merged_count`, `tracking_enabled`, `tracked_active_count`,
`matched_callsigns`, `matched_registrations`, `source_errors`, and `data_stale`.

Each normalized item in `flights` can contain `key`, `registration`, `hex`,
`callsign`, `source`, `aircraft_model`, `airline`, `alt_m`, `spd_kmh`,
`dist_km`, `dir_deg`, `latitude`, `longitude`, `position_age_s`,
`position_stale`, `category`, `squawk`, `tracked`, `tracked_by`, and
`tracked_target`. Fields depend on the source data.

The tracked-count sensor and binary sensor expose tracking state plus matched
callsigns/registrations. When a source fails, the last source data is retained,
`source_errors` is populated, and `data_stale` becomes `true`.

## Lovelace card

The integration automatically serves and registers its versioned bundle. A new
installation does not need a separate card repository or a manually added
resource:

```yaml
type: custom:air-traffic-card
entity: sensor.air_traffic_merged
title: Air Traffic
show_status: true
show_debug: false
show_counts: false
max_items: 25
compact: false
```

Existing dashboards may keep using the compatible legacy name:

```yaml
type: custom:air-traffic-merge-card
entity: sensor.air_traffic_merged
title: Air Traffic
max_items: 25
```

Both names use the same implementation. The card shows source counts, aircraft
rows, normalized metrics, stale/error state, and a selectable detail view. Its
layout changes from four metric columns to two on narrow cards. Home Assistant
theme variables are used, so light and dark themes are supported by the card's
CSS.

### Card options

| Option | Default | Meaning |
|---|---:|---|
| `entity` | required | Entity whose `flights` attribute is displayed |
| `title` | `Air Traffic` | Card heading |
| `show_status` | `true` | Show FR24, ADS-B, and merged counts |
| `show_debug` | `false` | Show the raw entity attributes as JSON |
| `show_counts` | `false` | Show `attributes.counts` when a source provides it; Air Traffic does not create this attribute itself |
| `max_items` | `25` | Maximum number of displayed flights |
| `compact` | `false` | Use the compact card-size hint |

The bundle is registered under the internal path
`/air_traffic_merge/air-traffic-card.js`. The integration registers it once and
does not write dashboards or `.storage/lovelace.resources`.

## Migration

The rename from **Air Traffic Merge** to **Air Traffic** is a public naming and
repository change, not a Home Assistant domain migration:

- Keep `air_traffic_merge` in the custom-component path and manifest.
- Keep existing Config Entries, entity IDs, unique IDs, and options.
- Update the existing HACS repository/install instead of creating a second
  integration entry.
- Keep `custom:air-traffic-merge-card` until the new bundle has been checked.
- Only change a dashboard copy to `custom:air-traffic-card` after verification.

The former standalone card repository is not automatically removed. Do not
delete its Lovelace resource or archive the old repository solely because the
new integration bundles a card. That cleanup requires a separately verified
migration and user decision.

## Updating

1. Create a Home Assistant backup.
2. Update Air Traffic through HACS to the desired published release.
3. Restart Home Assistant when HACS requests it.
4. Confirm the existing Config Entry and the three Air Traffic entities.
5. Open an existing dashboard and check the current or legacy card.

The current development version is not a published beta. Do not install it in
production merely because the version is visible in the source manifest.

## Troubleshooting

- **No aircraft:** check that the selected entity has a list-valued `flights`
  or `aircraft` attribute and that its state is not `unknown`/`unavailable`.
- **ADS-B URL error:** open the normalized URL from the Home Assistant host and
  confirm that it returns JSON with an `aircraft` list.
- **Stale source warning:** inspect `source_errors` and `data_stale` on
  `sensor.air_traffic_merged`; the last valid source data may still be shown.
- **Card not found:** reload the Home Assistant frontend and verify that the
  integration is loaded. Keep the old card resource until the new bundle is
  proven in the target installation.
- **Unexpected empty fields:** input schemas differ between providers; missing
  fields are intentionally not fabricated.

## Privacy and limitations

Air Traffic reads the configured Home Assistant entities and, in URL mode,
fetches the configured ADS-B endpoint locally. It does not provide a FR24 cloud
login, proxy credentials, map service, or flight-status enrichment. Provider
terms, rate limits, and any network exposure of a local ADS-B endpoint remain
the user's responsibility.

The card is a responsive list/detail card, not a geographic map. The exact
fields available depend on the configured source. Functional screenshots are
not included because no verified productive screenshot is available; the
repository images are branding assets only.

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening an issue or pull
request. Include the Home Assistant version, Air Traffic version, source mode,
minimal card YAML, and redacted logs. Never publish tokens, API keys, private
URLs, or precise personal location data.

## License

Air Traffic is released under the [MIT License](LICENSE).
