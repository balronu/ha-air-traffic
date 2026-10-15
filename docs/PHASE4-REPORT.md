# Air Traffic Phase 4 – Abschlussbericht

**Status:** lokale Migrationserweiterung abgeschlossen, vorbehaltlich der
nachfolgend aufgeführten blockierten HA-/CI-Gates  
**Branch:** `work/air-traffic-modernization`  
**Ausgangscommit:** `8e91e302b9fdcee6fcf3d2537b9f717336b4ec6c`  
**Implementation-Commit:** `29fcec79a6c0dd43fbefe1e301993d76d897eebd`  
**Dokumentations-Commit:** wird nach der Berichtaktualisierung eingetragen  
**Git-Status:** wird nach der Berichtaktualisierung abschließend geprüft

## Ergebnis

- Die interne Domain `air_traffic_merge` und die bestehenden Entity-/Unique-ID-
  Verträge bleiben unverändert.
- Backend-Attribute des bisherigen Sensors wurden im integrierten Kartenvertrag
  wieder vollständig berücksichtigt.
- `custom:air-traffic-card` und `custom:air-traffic-merge-card` registrieren
  dieselbe aktuelle Kartenlogik idempotent.
- Die Legacy-Kartenparameter einschließlich des historischen Defaults
  `max_items: 25` bleiben erhalten.
- Es wurden keine produktiven HA-Daten, Dashboards, Remote-Repositories,
  Releases oder Tags verändert.

## Teststatus

| Prüfung | Status | Bemerkung |
|---|---|---|
| Python-Kompatibilitätsverträge | PASS | lokale Offline-Tests |
| Frontend-Kompatibilitätsverträge | PASS | Vitest |
| Frontend-Build/Syntax | PASS | lokales Node/Vite |
| HA-Fixture mit Config Entry/Registry | BLOCKED | lokales Tooling fehlt |
| Reload/Unload in HA | BLOCKED | HA-Fixture fehlt |
| Hassfest | BLOCKED | CI-Workflow vorbereitet |
| HACS-Validierung | BLOCKED | CI-Workflow vorbereitet |
| Gitleaks | NOT RUN | lokales Binary fehlt |
| Produktive Migration | NOT RUN | nicht autorisiert |

## Offene Risiken und Empfehlung

Die automatische HACS-Weiterleitung bei einer späteren Repository-Umbenennung
ist nicht bewiesen. Die Umbenennung sollte erst nach einem freigegebenen,
CI-geprüften Release und einer dokumentierten manuellen Fallback-Anleitung
erfolgen. Das alte Kartenrepository sollte bis zur bestätigten Umstellung weder
archiviert noch gelöscht werden.

Phase 5 wurde nicht begonnen.
