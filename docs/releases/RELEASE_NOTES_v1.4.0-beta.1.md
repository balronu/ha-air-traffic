# Air Traffic v1.4.0-beta.1 (draft)

> Draft only. No release or tag has been published.

## English

### Highlights

- Consolidated backend and Lovelace card candidate under the Air Traffic brand.
- Added versioned, automatically served frontend bundle.
- Preserved `air_traffic_merge`, existing entities, unique IDs and legacy card type.
- Added retry/backoff, source-error isolation, stale-data markers and deduplication.
- Added responsive aircraft list/detail rendering and migration documentation.

### Compatibility

Existing Config Entries and dashboards must be kept. The legacy card type
`custom:air-traffic-merge-card` remains supported. Validate the bundle after
installation before removing any old Lovelace resource.

### Validation

Offline tests pass. HA fixture, Hassfest, HACS validation and secret scanning
remain release gates and must pass in CI before publication.

## Deutsch

### Höhepunkte

- Backend und Lovelace-Karte als lokaler Kandidat unter dem Namen Air Traffic
  zusammengeführt.
- Versioniertes, automatisch bereitgestelltes Frontend-Bundle ergänzt.
- `air_traffic_merge`, bestehende Entities, Unique IDs und Legacy-Kartentyp
  erhalten.
- Wiederholungen, Quellfehler-Isolation, Stale-Markierungen und Deduplizierung
  ergänzt.
- Responsive Flugzeugliste/Detailansicht und Migrationsdokumentation ergänzt.

### Kompatibilität

Bestehende Config Entries und Dashboards müssen erhalten bleiben. Der Legacy-Typ
`custom:air-traffic-merge-card` bleibt unterstützt. Vor dem Entfernen alter
Lovelace-Ressourcen muss das neue Bundle geprüft werden.

### Validierung

Offline-Tests bestehen. HA-Fixture, Hassfest, HACS-Validierung und Secret Scan
bleiben Release-Gates und müssen vor Veröffentlichung in CI bestehen.
