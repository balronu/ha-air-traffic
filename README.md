<p align="center">
  <img src="images/branding/air-traffic-logo.png" alt="Air Traffic logo" width="180">
</p>

<p align="center">
  <img src="images/branding/air-traffic-readme-banner.png" alt="Air Traffic – Home Assistant integration with built-in Lovelace card">
</p>

# Air Traffic

Air Traffic is a Home Assistant custom integration that combines an existing
Flightradar24 sensor with local ADS-B data and ships its Lovelace card in the
same integration bundle.

> **Current status:** the repository is now `balronu/ha-air-traffic` and the
> merged `main` branch is preparing the `1.4.0-beta.1` pre-release. The beta
> tag and GitHub release are published only after the final isolated card test.

## Contents

- [Features](#features)
- [Supported data sources](#supported-data-sources)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Lovelace card](#lovelace-card)
- [Migration from Air Traffic Merge](#migration-from-air-traffic-merge)
- [Updating](#updating)
- [Troubleshooting](#troubleshooting)
- [Privacy and data sources](#privacy-and-data-sources)
- [Known limitations](#known-limitations)
- [Screenshots](#screenshots)
- [Contributing and support](#contributing-and-support)
- [License](#license)

## Features

- FR24-only, ADS-B-only, or combined source mode
- ADS-B data from a URL returning `aircraft.json`
- ADS-B data from an existing Home Assistant sensor with an `aircraft` attribute
- Normalization, source merging and duplicate suppression
- Tracking by callsign, registration, or both
- Shared `DataUpdateCoordinator` with retries and non-blocking source errors
- Invalid coordinates and stale ADS-B positions are marked or discarded safely
- Built-in responsive Lovelace card with empty, unavailable, error and stale states
- Aircraft selection and detail view
- Light/dark theme variables and legacy card compatibility

## Supported data sources

### Flightradar24 entity

The selected Home Assistant sensor must expose a `flights` list in its state
attributes. Air Traffic does not call a Flightradar24 API and does not provide
FR24 credentials.

### ADS-B URL

The configured URL must return JSON containing an `aircraft` list, such as a
local `readsb`/`tar1090` endpoint. If a host URL is entered, the integration
normalizes it to `/data/aircraft.json`.

### ADS-B entity

The selected Home Assistant sensor must expose an `aircraft` list in its state
attributes. `messages` and `now` are retained when supplied by the source.

Missing values remain missing; the integration does not invent aircraft,
coordinates, routes, airport names or flight status.

## Requirements

- A current Home Assistant version compatible with the release being installed
- HACS, or permission to install a custom component manually
- At least one supported data source
- Network access from Home Assistant to the configured local ADS-B endpoint when
  URL mode is used

## Installation

### HACS

The HACS source is `balronu/ha-air-traffic`. After the `1.4.0-beta.1`
pre-release is published, install **Air Traffic** from
**HACS → Integrations**, restart Home Assistant, and add it under
**Settings → Devices & services**. Until then, use the local development
workflow or manual installation.

### Manual installation

For a release or local checkout, copy the directory
`custom_components/air_traffic_merge` into Home Assistant's
`/config/custom_components/` directory and restart Home Assistant. Keep the
directory name `air_traffic_merge`; it is an intentional compatibility
identifier.

## Configuration

Add the integration from **Settings → Devices & services → Add integration**
and select **Air Traffic**. The flow offers FR24, ADS-B, or both; FR24 entity
selection; ADS-B URL or entity; scan interval; and optional tracking by
callsign/registration.

The internal Home Assistant domain remains `air_traffic_merge`. Existing
Config Entries, entities, unique IDs and options are not renamed.

## Lovelace card

The integration automatically serves and registers the versioned frontend
bundle. A second card repository is not required for a new installation.

```yaml
type: custom:air-traffic-card
entity: sensor.air_traffic_merged
title: Air Traffic
show_status: true
show_debug: false
show_counts: true
max_items: 25
compact: false
```

Existing dashboards may continue to use the legacy type:

```yaml
type: custom:air-traffic-merge-card
entity: sensor.air_traffic_merged
```

Both names use the same current implementation. Registration is idempotent and
the integration does not edit `.storage/lovelace.resources` or overwrite
dashboards. The current bundle URL is:

```text
/air_traffic_merge/air-traffic-card.js?v=1.4.0-beta.1
```

### Card options

| Option | Default | Description |
|---|---:|---|
| `entity` | required | Merged Air Traffic sensor |
| `title` | `Air Traffic` | Card heading |
| `show_status` | `true` | Source and merged counts |
| `show_debug` | `false` | Raw attributes for diagnosis |
| `show_counts` | `false` | Optional category-count display when supplied |
| `max_items` | `25` | Maximum displayed flights |
| `compact` | `false` | Compact card sizing hint |

## Migration from Air Traffic Merge

The public name changes to **Air Traffic**, but the internal domain remains
`air_traffic_merge` to protect existing installations. Do not delete and
recreate the integration entry merely because the public repository name
changes.

The legacy card type `custom:air-traffic-merge-card` remains registered. After
confirming the new bundle works, users may optionally change a copied dashboard
to `custom:air-traffic-card`. Existing Lovelace resources are not removed
automatically. See [the Phase 4 migration guide](docs/PHASE4-MIGRATION.md).

## Updating

Back up Home Assistant before updating. After an update, verify the main entity,
the card and the source status. The bundle URL contains a version query string
so browsers can refresh it after a frontend update. The beta release is
published only after the isolated Lovelace test gate passes.

## Troubleshooting

- **No flights:** verify the selected entity and that it exposes `flights` or
  `aircraft` as a list.
- **ADS-B URL errors:** open the endpoint from the Home Assistant host and
  confirm a JSON response containing `aircraft`.
- **Stale data:** inspect `data_stale` and `source_errors` on the merged sensor.
- **Card not found:** reload the Home Assistant frontend after confirming the
  integration is loaded; do not remove the existing resource until verified.
- **Missing attributes:** source formats vary. Missing fields are shown as
  unavailable rather than fabricated.

## Privacy and data sources

Air Traffic processes data exposed by the configured Home Assistant entity or
ADS-B endpoint. It does not proxy FR24 credentials and has no built-in cloud
account. Local network traffic remains subject to each provider's terms and
rate limits.

## Known limitations

- The current card is a responsive aircraft list/detail view; it does not claim
  to provide a geographic map or map zoom engine.
- A live Home Assistant fixture, Hassfest and HACS validation are release gates
  and were not available in the local environment.
- The exact field set depends on the configured source.

## Screenshots

No screenshots are included as functional evidence yet. A productive Home
Assistant instance or isolated HA fixture was not available, and generated or
simulated screens must not be presented as real behavior. The generated
branding assets in `images/branding/` are visual project assets only.

## Contributing and support

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull
request. Include the Home Assistant version, integration version, source mode,
a redacted error, and a minimal card configuration. Never post API keys,
tokens, private URLs or personal location data.

## License

Air Traffic is released under the [MIT License](LICENSE).
