# Air Traffic Phase 1 – Bestandsaufnahme

**Datum:** 2026-10-15  
**Arbeitsbranch:** `work/air-traffic-modernization`  
**Ausgangs-Commit:** `39c36f5a297502a1dd1f7f12e147909382d6a600`  
**Status:** Analyse abgeschlossen; keine Veröffentlichung, kein Merge und keine produktive Home-Assistant-Änderung

## 1. Repository-Bestand

| Projekt | Repository | Default/Arbeitsstand | Veröffentlichung | Lizenz | Status |
|---|---|---|---|---|---|
| Integration | `balronu/air-traffic-merge` | `main`, `v1.3.1`, Commit `39c36f5` | `v1.3.1` am 2026-06-10 | MIT | nicht archiviert |
| Karte | `balronu/air-traffic-merge-card` | `main`, `v1.1.1`, Commit `8f46a14` | `v1.1.1` am 2026-06-10 | MIT | nicht archiviert |
| Referenz | `balronu/ha-mobile-fuel-stations` | aktueller lokaler Analyse-Checkout `feature/brand-logo-expansion-prep`, Commit `aea1fdf` | `v0.6.0` stabil; mehrere Beta-Releases | MIT | nicht archiviert |
| Referenz | `balronu/ha-camper-travel-journal` | lokaler Analyse-Checkout `docs/readme-roadmap-beta10`, Commit `df50d97` | `v0.1.0-beta.10`; Beta 11 vorbereitet, nicht veröffentlicht | MIT | nicht archiviert |
| Ziel | `balronu/ha-air-traffic` | existiert am Analysedatum nicht (GitHub 404) | keine | — | keine Änderungen vorgenommen |

Das tatsächliche Repository des Camper Travel Journal ist somit
`balronu/ha-camper-travel-journal`.

## 2. Ausgangssicherheit

- Die vier relevanten lokalen Projektklone waren vor der Analyse sauber; es gab
  keine ungesicherten Änderungen in ihnen.
- Der übergeordnete Workspace enthält zahlreiche unabhängige unversionierte
  Arbeitsartefakte. Diese wurden nicht bereinigt, verschoben oder überschrieben.
- Der Integrations-Checkout arbeitet nun auf dem lokalen Branch
  `work/air-traffic-modernization`.
- Es wurden keine Remote-Branches, Tags, Releases, Issues, Repository-Namen oder
  produktiven HA-Daten geändert.
- Die historischen Branches und Tags der Referenzprojekte wurden nur gelesen.

## 3. Tatsächliche Integration

### Dateien und Architektur

`air-traffic-merge` enthält nur eine kleine Custom Integration:

- `__init__.py`: forwardet `sensor` und `binary_sensor`; kein zentraler
  Coordinator-Lifecycle.
- `config_flow.py`: sechsstufiger Flow für FR24-Entity, ADS-B-URL oder
  ADS-B-Entity und Tracking.
- `coordinator.py`: enthält eine eigene Zusammenführungsklasse mit URL-/Entity-
  und FR24-Unterstützung, wird aber aus dem aktiven Setup nicht instanziiert.
- `sensor.py`: enthält eine zweite, aktive Polling-Implementierung.
- `binary_sensor.py`: liest einen gemeinsamen In-Memory-Store.
- keine Tests, kein `pyproject.toml`, kein Frontend-Quellprojekt und kein
  integriertes Frontend-Bundle.

### Aktive Laufzeitabweichung

Die aktive `sensor.py`-Implementierung:

- liest ausschließlich `entry.data["adsb_url"]`;
- ignoriert im laufenden Betrieb `source_mode`, FR24-Entity und ADS-B-Entity;
- erzeugt pro Polling-Zyklus eine neue `aiohttp.ClientSession`;
- fängt alle Fehler pauschal ab und ersetzt die Attribute durch ein Fehlerobjekt;
- verwendet einen eigenen Timer statt `DataUpdateCoordinator`;
- liefert nur die ADS-B-Felder `flight`, `r`, `hex`, `t`, `alt_baro`, `gs`,
  `r_dst` und `r_dir` in die Kartenstruktur;
- feuert keine Tracking-Ereignisse.

Der vorhandene `coordinator.py` ist deshalb keine verlässliche Beschreibung des
tatsächlichen Produktverhaltens. Er ist ein möglicher Ausgangspunkt, aber kein
Beweis dafür, dass FR24 + ADS-B aktuell funktionieren.

### Datenzusammenführung im ungenutzten Coordinator

- ADS-B wird primär per Registrierung, ersatzweise per HEX-Schlüssel indiziert.
- FR24 wird ausschließlich per `aircraft_registration` indiziert.
- Doppelte Datensätze werden nur erkannt, wenn die Schlüssel exakt passen.
- Fehlende Registrierungen, abweichende Schreibweisen und fehlende HEX-Werte
  können daher zu Duplikaten oder zu nicht zusammengeführten Flugzeugen führen.
- FR24-Daten werden nur teilweise übernommen; Herkunft, Ziel, Status und viele
  Positionsfelder werden nicht modelliert.
- HTTP-Fehler und JSON-Fehler werden still als `None` behandelt; es gibt keine
  verwertbare Diagnose, Backoff-Strategie oder Stale-Data-Semantik.

## 4. Tatsächliche Karte

`air-traffic-merge-card` enthält ein einzelnes, bereits gebündeltes
`dist/air-traffic-merge-card.js` ohne Quellcode, Paketmanifest oder Frontend-Tests.

Vorhandene Funktionen:

- Kartenzeilen für Callsign, Registrierung, Quelle, Entfernung, Höhe,
  Geschwindigkeit und Kurs;
- Statusblock für FR24/ADS-B;
- optionale Kategorie-Chips und Debug-Ausgabe;
- Tracking-Badge;
- einfache responsive CSS-Regeln und Home-Assistant-CSS-Variablen;
- HTML-Escaping für angezeigte Textwerte.

Fehlende bzw. nicht nachgewiesene Funktionen:

- keine interaktive Karte oder Flugzeugauswahl;
- keine Detailansicht, Suchfunktion oder Kartenebenen;
- kein visueller Karteneditor;
- kein idempotenter `customElements.get()`-Schutz;
- kein `window.customCards`-Katalog;
- keine Lade-, Fehler-, Verbindungsunterbrechungs- oder Stale-Data-Zustände
  mit eigener UX;
- keine Mehrfachimport-, Reload-, Cache- oder Versionswechseltests.

Die aktuelle Karte registriert `customElements.define("air-traffic-merge-card", …)`
unbedingt. Ein zweiter Import kann dadurch einen `NotSupportedError` auslösen.

## 5. Namens- und Kompatibilitätsrisiken

Aktuelle technische Kennungen:

- Domain: `air_traffic_merge`
- Config-Flow-Titel: `Air Traffic Merge`
- Entity-Namen: `Air Traffic Merged`, `Air Traffic Tracked Count`,
  `Air Traffic Tracked Present`
- Ereignis: `air_traffic_merge_tracked`
- Karten-Element: `air-traffic-merge-card`
- HACS-Kartenpfad: `/hacsfiles/air-traffic-merge-card/dist/air-traffic-merge-card.js`
- Integrationspfad: `custom_components/air_traffic_merge`

Eine direkte Umbenennung auf die neue Domain `air_traffic` würde den bisherigen
Config-Entry nicht automatisch übernehmen. Entity-Registry-Einträge, Entity IDs,
Unique IDs, Optionen und Dashboard-Ressourcen sind getrennte Persistenzobjekte.
Ein `async_migrate_entry` innerhalb einer neuen Domain reicht nicht aus, um einen
Config-Entry aus der alten Domain sicher umzuhängen.

**Vorläufige Architekturentscheidung für Phase 2:** öffentliche Namen und neue
Repository-/Frontend-Namen auf **Air Traffic** umstellen, die alte Domain
`air_traffic_merge` jedoch zunächst als technische Kompatibilitätsdomäne
beibehalten oder einen ausdrücklich getesteten Import-/Migrationsmechanismus
entwickeln. Eine Domain-Umbenennung darf erst nach einem belastbaren
Config-Entry-/Entity-Registry-Test entschieden werden.

Die bestehenden Entity-Unique-IDs basieren auf `entry.entry_id`; das hilft bei
einem unveränderten Config-Entry, ersetzt aber keine Domain-Migration.

## 6. Referenzvergleich

### Mobile Fuel Stations

- versionierte Frontend-Konstanten und URL, z. B.
  `/<domain>/<bundle>?v=<version>`;
- einmalige Registrierung mit `hass.http.async_register_static_paths` und
  `add_extra_js_url`;
- `cache_headers=False` für das statische Bundle;
- zentraler `DataUpdateCoordinator` mit Lifecycle und Reload-Listener;
- TypeScript-Quellcode, reproduzierbarer Vite-Build, Lockfile und gebündelte
  Datei unter dem Integrationspfad;
- Python- und Frontend-Tests, Build-Diff-Prüfung, Hassfest und Gitleaks;
- README.de/README.en, Branding-Assets, Issue-Formulare und PR-Template.

### Camper Travel Journal

- dieselbe integrationseigene Static-Path-/Extra-JS-Strategie;
- idempotente Registrierung aller Custom Cards über `window.customCards`;
- `customElements.get()`-Schutz und Lifecycle-/Browser-Regressionstests;
- versionierte Bundle-Verträge zwischen Manifest, npm-Paket, Lockfile und URL;
- dokumentierte Cache-/Resource-Grenzen ohne direkte Manipulation von
  `.storage/lovelace.resources`;
- Hassfest, HACS-Strukturprüfung, Secret-Scan, Coverage und Chromium-Harness;
- getrennte deutsche/englische Dokumentation und Release-Workflow.

Diese Muster sind geeignete technische Referenzen. Sie autorisieren keine
Änderung an den Referenzprojekten.

## 7. Datenquellen und Nutzungsbedingungen – Analysebedarf

Im aktuellen Code sind nur diese Quellen nachgewiesen:

1. ein vorhandener Home-Assistant-Sensor mit `flights`-Attribut, der als FR24
   bezeichnet wird;
2. lokale `aircraft.json`-Daten, typischerweise readsb/tar1090/adsb.im;
3. ein vorhandener Sensor mit `aircraft`-Attribut.

Es gibt keinen API-Client für FlightRadar24, keinen dokumentierten externen
FR24-API-Vertrag und keine nachgewiesene Flugstatus-/Flughafen-/Flugzeugbild-
Anreicherung. README-Aussagen müssen daher strikt auf diese tatsächlich
implementierten Datenverträge begrenzt werden, bis Quellen und Nutzungsrechte
separat verifiziert sind.

## 8. GitHub-/CI-Bestand

Die Air-Traffic-Repositories haben jeweils nur einen `Validate`-Workflow:

- Integration: Python-Compileall und JSON-Parsing;
- Karte: Node-Syntaxprüfung und JSON-Parsing.

Es existieren keine automatisierten Backend- oder Frontend-Tests, kein Hassfest,
keine HACS-Strukturprüfung, kein Secret-Scanning, kein Build-/Bundle-
Synchronitätscheck und kein Release-Workflow. Beide Projekte haben keine offenen
Issues und keine zusätzlichen Entwicklungsbranches im Remote-Bestand. Die letzten
Releases sind `v1.3.1` und `v1.1.1`; die Tags `public-release` verweisen auf die
frühen `v1.0.0`-Releaseobjekte.

## 9. Baseline-Checks am 2026-10-15

| Prüfung | Ergebnis | Anmerkung |
|---|---|---|
| Integration `python3 -m compileall` | PASS | lokaler Ausgangsstand |
| Integration JSON-Parsing | PASS | alle versionierten JSON-Dateien |
| Kartenbundle `node --check` | PASS | vorhandenes Dist-Bundle |
| Karten-JSON-Parsing | PASS | `hacs.json` |
| `git diff --check` | PASS | beide Projektklone sauber |
| Python-Testsuite Air Traffic | NOT RUN | keine Tests im Repository; `pytest` nicht verfügbar |
| Frontend-Testsuite Air Traffic | NOT RUN | keine Quell-/Teststruktur vorhanden |
| Hassfest | NOT RUN | kein lokaler/CI-Gate im Bestand ausgeführt |
| HACS-Validierung | NOT RUN | kein vorhandenes Gate |
| Secret-Scan | NOT RUN | `gitleaks` nicht verfügbar |
| Produktive HA-Prüfung | NOT RUN | ausdrücklich ausgeschlossen |
| Echte Desktop-/iPhone-Screenshots | NOT RUN | keine produktive Installation verwendet |

## 10. Entscheidungen vor irreversiblen Schritten

Vor einem späteren Merge in `main`, Repository-Rename, Archivierung des
Kartenrepositories, Tagging oder Release sind weiterhin ausdrücklich erforderlich:

1. Entscheidung über technische Beibehaltung von `air_traffic_merge` versus
   getestete Domain-Migration auf `air_traffic`;
2. verifizierte Datenquellenverträge und zulässige Nutzungsbedingungen;
3. getesteter Importpfad für bestehende Config Entries, Optionen, Entities und
   Lovelace-Konfigurationen;
4. vollständige Backend-/Frontend-/HA-Fixture-Tests;
5. reale Screenshots aus einer freigegebenen Testinstallation;
6. ausdrückliche Freigabe für öffentliche Repository-/Release-Aktionen.

## 11. Assets

Die vom Auftraggeber bereitgestellte Bildreferenz wurde nur als Designreferenz
verwendet. In Phase 1 wurden keine Logos, Social-Preview-Dateien oder
Funktions-Screenshots erzeugt bzw. als reale Produktnachweise ausgegeben.
