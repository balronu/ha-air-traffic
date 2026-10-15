# Air Traffic Phase 2 – Zusammenführung

**Branch:** `work/air-traffic-modernization`  
**Basis:** `39c36f5a297502a1dd1f7f12e147909382d6a600`  
**Kandidat:** `1.4.0-beta.1`  
**Scope:** lokale Backend-/Frontend-Zusammenführung; kein Push, Merge, Release,
Repository-Erstellen, HA-Installieren oder Dashboard-Ändern

## Zusammengeführte Komponenten

- Die bisher ungenutzte Coordinator-Logik wurde durch eine aktive
  `DataUpdateCoordinator`-Pipeline ersetzt.
- FR24-Entity, ADS-B-URL und ADS-B-Entity werden entsprechend dem Config Flow
  tatsächlich gelesen.
- ADS-B- und FR24-Datensätze werden normalisiert und über Registrierung bzw.
  HEX/Callsign zusammengeführt, wenn eine stabile Identität vorhanden ist.
- Die Sensoren und der Binary Sensor lesen ausschließlich den gemeinsamen
  Coordinator-Snapshot; die doppelte Polling-Implementierung wurde entfernt.
- Die Karte liegt nun unter
  `custom_components/air_traffic_merge/frontend/air-traffic-card.js` und wird
  über ein reproduzierbares TypeScript/Vite-Projekt gebaut.

## Funktionierende Datenquellen im Kandidaten

| Quelle | Implementiert | Offline getestet | HA-Laufzeittest |
|---|---:|---:|---:|
| FR24 Home-Assistant-Entity mit `flights` | PASS | PASS (Normalisierung/Merge) | BLOCKED |
| ADS-B URL mit `aircraft`-Liste | PASS | PASS (Normalisierung/Merge-Vertrag) | BLOCKED |
| ADS-B Home-Assistant-Entity mit `aircraft` | PASS | PASS (Normalisierung/Merge-Vertrag) | BLOCKED |
| FR24 + ADS-B Deduplication | PASS | PASS, Registrierung identifiziert ein Flugzeug einmal | BLOCKED |

Die Quellen wurden nicht gegen eine produktive Instanz oder ein externes
Flugverkehrs-API getestet. Der Code behauptet keine FR24-API-Anbindung.

## Behobene Architekturfehler

- Der aktive Sensor ignoriert nicht mehr die im Config Flow angebotenen Quellen.
- Es gibt keine zweite, konkurrierende Polling-/Store-Implementierung mehr.
- HTTP-Sessions werden aus Home Assistants Session-Manager verwendet und
  Responses per Context Manager geschlossen.
- Fehler werden als `source_errors` und `data_stale` sichtbar; erfolgreiche
  Quelldaten bleiben bei einem Teilfehler als Stale-Daten erhalten.
- Tracking, Tracked-Count und Binary Sensor stammen aus demselben Snapshot.
- Unload und Options-Reload laufen über den Coordinator-Lifecycle.
- Fehlende Datenfelder bleiben leer/`None` und werden nicht erfunden.

## Kartenkompatibilität und Registrierung

- Neuer Kartentyp: `custom:air-traffic-card`.
- Alter Kartentyp: `custom:air-traffic-merge-card` bleibt als separate
  Legacy-Custom-Element-Klasse erhalten.
- Beide Registrierungen prüfen `customElements.get()`.
- `window.customCards` wird pro Typ nur einmal ergänzt.
- Das Bundle wird einmalig über `async_register_static_paths` und
  `add_extra_js_url` registriert.
- Die URL ist versionsgebunden:
  `/air_traffic_merge/air-traffic-card.js?v=1.4.0-beta.1`.
- `.storage/lovelace.resources` wird nicht verändert.

## Tests

| Test | Ergebnis | Evidenz |
|---|---|---|
| Python Compileall | PASS | `python3 -m compileall` |
| Backend-Daten-/Merge-Tests | PASS | 5/5 `unittest` |
| Integrations-/Bundle-Vertragstests | PASS | 3/3 `unittest` |
| Frontend-Lifecycle-/Render-Tests | PASS | 2/2 Vitest |
| TypeScript/Vite-Build | PASS | Bundle erzeugt |
| Bundle JavaScript-Syntax | PASS | `node --check` |
| JSON-Validierung | PASS | alle Projekt-JSON-Dateien |
| `git diff --check` | PASS | Kandidat ohne Whitespace-Fehler |
| Hassfest gegen HA 2026.10.1 | BLOCKED | pip/venv/ensurepip fehlen lokal |
| pytest-homeassistant Fixture | BLOCKED | HA-Testumgebung konnte nicht installiert werden |
| Gitleaks | NOT RUN | Binary nicht verfügbar |
| Produktive HA-/Dashboard-Prüfung | NOT RUN | ausdrücklich ausgeschlossen |

## Offene Punkte vor Phase 3

1. HA 2026.10.1 in einer geeigneten CI- oder lokalen Python-Umgebung ausführen
   und Config Flow, Coordinator, Static-Path-Registrierung, Reload/Unload sowie
   Entity-Kompatibilität als echte HA-Tests prüfen.
2. Hassfest, HACS-Strukturprüfung und Secret-Scan ausführen.
3. Reale Screenshots erst in einer freigegebenen Testinstallation erstellen.
4. Datenquellen- und Nutzungsbedingungen separat dokumentieren.
5. GitHub-Zielrepository, Push, Merge, Tag und Release bleiben bis zur
   ausdrücklichen Freigabe offen.
