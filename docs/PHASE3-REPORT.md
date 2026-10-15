# Air Traffic Phase 3 – Technische Modernisierung

**Branch:** `work/air-traffic-modernization`  
**Ausgangscommit:** `1133b192f90179b2d777834930b1fed43f9bc734`  
**Implementation commit:** `e10047dbb3d49ef8d3983cf2d7d1b2b703cf5801`  
**Git-Status:** sauber  
**Status:** lokale Kandidatenarbeit abgeschlossen; Phase 4 nicht begonnen

## Behobene Fehler

- Ein einzelner Quellenausfall blockiert die Integration nicht mehr: Es wird ein
  verfügbarer Snapshot mit `source_errors` und `data_stale` bereitgestellt.
- ADS-B-HTTP-Abfragen verwenden drei Versuche mit exponentiellem Backoff für
  Timeouts, Netzwerkfehler, HTTP 429 und HTTP-5xx.
- HTTP-Antworten werden geschlossen; der Home-Assistant-Session-Manager bleibt
  zuständig für die Client-Session.
- Nicht verfügbare Home-Assistant-Entities werden sauber als Quellfehler
  behandelt.
- Ungültige/nicht endliche Koordinaten werden verworfen.
- ADS-B-Positionen mit `seen_pos`/`seen` über 300 Sekunden werden als veraltet
  markiert.
- Wiederholte Meldungen desselben Flugzeugs innerhalb einer Quelle werden nicht
  doppelt ausgegeben.
- Die Karte besitzt eine Auswahl-/Detailansicht ohne globale Event-Listener;
  Lit verwaltet die Listener im Komponentenlebenszyklus.

## Backend-Änderungen

- `DataUpdateCoordinator` bleibt die einzige aktive Polling-Pipeline.
- FR24-Entity, ADS-B-URL und ADS-B-Entity werden getrennt gelesen.
- Priorität der Identität: Registrierung, dann HEX, dann Callsign.
- Vorhandene Entity-Namen, Unique IDs, Domain `air_traffic_merge`, Config Entries
  und Ereignisname bleiben erhalten.
- Mindestintervall bleibt bei fünf Sekunden, um unbeabsichtigte Request-Stürme
  zu vermeiden.

## Frontend-Änderungen

- Responsive Container-Layouts für schmale und breite Karten.
- Nutzung von Home-Assistant-Theme-Variablen.
- Leere, nicht verfügbare, Fehler- und veraltete Datenzustände.
- Auswahl eines Flugzeugs und Detailansicht für Identität, HEX, Position und
  Datenalter.
- Neuer Typ `custom:air-traffic-card` und kompatibler Typ
  `custom:air-traffic-merge-card`.
- Keine vorhandene interaktive geografische Karte wurde vorgetäuscht: Der
  Ausgangsstand besaß keine Karten-/Zoom-Engine. Eine echte Kartenebene bleibt
  ein späteres, separat zu bewertendes Feature.

## Testumgebung

Die lokale Laufzeit bietet Python 3.13, aber kein `pip`, `ensurepip` oder
`python3-venv`; Podman, Docker, `act` und Gitleaks sind ebenfalls nicht
verfügbar. Ein isolierter venv-/pip-Versuch wurde deshalb BLOCKED beendet und
hat keine System- oder HA-Pakete installiert. Für die fehlenden Gates wurden
`.github/workflows/tests.yml` und `.github/workflows/validate.yml` vorbereitet.
Sie installieren HA 2026.10.1 ausschließlich in GitHub Actions und führen
pytest, Hassfest, Frontend-Build, HACS-Vertragsprüfung und Gitleaks aus. Wegen
der ausdrücklichen Push-Sperre wurden die Workflows nicht remote gestartet.

## Testergebnisse

| Prüfung | Ergebnis | Nachweis |
|---|---|---|
| Backend-/Vertragstests | PASS | 10/10 `unittest` |
| Frontend-Tests | PASS | 2/2 Vitest |
| TypeScript/Vite-Build | PASS | Bundle neu erzeugt |
| Bundle-Syntax | PASS | `node --check` |
| Python Compileall | PASS | lokale Python-3.13-Laufzeit |
| JSON-Validierung | PASS | Projektdateien ohne `node_modules` |
| Diff-Check | PASS | Quell-/Dokumentationsdateien; generiertes Minified-Bundle ausgenommen |
| HA 2026.10.1 Runtime-Fixture | BLOCKED | lokale pip/venv-Werkzeuge fehlen |
| Hassfest | BLOCKED | nur vorbereiteter GitHub-Actions-Gate |
| HACS-Validierung | BLOCKED | nur vorbereiteter GitHub-Actions-Gate |
| Gitleaks | NOT RUN | Binary fehlt lokal, CI-Gate vorbereitet |
| Produktive HA-/Dashboard-Prüfung | NOT RUN | ausdrücklich ausgeschlossen |

## Tatsächlich abgesicherte Datenquellen

Offline abgesichert sind die Formate für FR24-Entities mit `flights`, ADS-B-
Entities mit `aircraft` und ADS-B-URLs mit `aircraft`. Die echte HA-Entity-
Lebensdauer, HTTP-Session, Coordinator-Reload und HA-API-Kompatibilität konnten
ohne Home-Assistant-Testumgebung nicht live ausgeführt werden. Deshalb sind die
Quellmodi **implementiert und offline geprüft**, aber nicht als produktiv live
verifiziert zu bezeichnen.

## Verbleibende Risiken

1. Hassfest kann API-/Manifestdetails melden, die ohne HA-Core nicht erkennbar
   sind.
2. Config-Flow-, Options-Flow-, Reload- und Unload-Tests benötigen eine echte
   HA-Fixture.
3. Die Legacy-Karte ist über den Custom-Element-Alias kompatibel; eine reale
   historische Dashboard-Ressource wurde nicht geladen.
4. FR24-/ADS-B-Feldvarianten außerhalb der getesteten Verträge können weitere
   Adapter benötigen.
5. Es gibt weiterhin keine echte geografische Kartenebene oder Zoomfunktion.

## Abschluss

Der finale lokale Stand enthält diesen Implementierungscommit plus die
Berichtsaktualisierung; der Git-Status ist sauber. Es gab keinen Push, Merge,
Release, Repository-Rename,
Archivierung, HA-Installationsversuch oder Dashboard-/Produktivänderung.
