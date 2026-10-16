# Air Traffic v1.4.0-beta.1

This is a GitHub pre-release for the consolidated Air Traffic integration and
Lovelace card. It is not a stable release.

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

The merged candidate passed the isolated Home Assistant 2026.10.1 /
Playwright browser gate, standalone production-bundle checks, Python tests,
frontend tests/build, Hassfest, HACS structure validation, and secret scanning.
The browser evidence covers both card types, automatic registration, entity
slug handling, aircraft selection/update, source-error/stale/empty states,
responsive rendering and light/dark themes.

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

Der zusammengeführte Kandidat bestand die isolierte Home-Assistant-2026.10.1- /
Playwright-Browserprüfung, die eigenständige Bundle-Prüfung, Python-Tests,
Frontend-Tests/Build, Hassfest, HACS-Strukturprüfung und Secret Scan. Die
Browser-Evidenz deckt beide Kartentypen, automatische Registrierung,
Entity-Slug-Verarbeitung, Flugauswahl/-aktualisierung, Quellfehler/Stale-/Leer-
Zustände sowie responsive Darstellung und helle/dunkle Themes ab.
