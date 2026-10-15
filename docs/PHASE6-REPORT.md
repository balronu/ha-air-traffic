# Air Traffic – Phase 6 Qualitätssicherung und Release-Vorbereitung

**Branch:** `work/air-traffic-modernization`  
**Ausgangscommit:** `03038a555b6fc25e73d70ecd827d4058c3d74e91`  
**Commit-SHA:** wird nach dem lokalen Abschluss eingetragen  
**Git-Status:** wird nach dem lokalen Abschluss geprüft  
**Gesamtbewertung:** **NOT READY FOR BETA**

## Zusammenfassung

Die lokal ausführbaren Prüfungen bestehen. Die Bewertung ist trotzdem **NOT
READY FOR BETA**, weil die verpflichtenden Home-Assistant-Fixture-, Hassfest-,
HACS- und Gitleaks-Prüfungen für den exakten Kandidaten nicht ausgeführt werden
konnten. Der Branch wurde nicht gepusht, daher kann GitHub Actions diesen
Kandidaten nicht prüfen. Es gab keine produktive HA-, Dashboard-, GitHub-
Repository-, Tag- oder Release-Änderung.

## Testmatrix

| Prüfung | Status | Tatsächlicher Nachweis / Grund |
|---|---|---|
| Backend- und Migrationstests | PASS | 14/14 `unittest` lokal |
| Frontend-Tests | PASS | 3/3 Vitest lokal |
| TypeScript/Vite-Build | PASS | `npm run build` lokal |
| Frontend-Bundle-Synchronität | PASS | Build erzeugt keinen Bundle-Diff |
| Bundle-Syntax | PASS | `node --check` |
| Python Compileall | PASS | `python3 -m compileall` |
| JSON-Validierung | PASS | alle Projekt-JSON-Dateien |
| Markdown-Links | PASS | lokale Referenzen in beiden READMEs |
| Bilddateien/Abmessungen | PASS | Logo 1024², Social 1280×640, Banner 1600×533 |
| HACS-/Manifest-Strukturvertrag | PASS | lokaler Struktur- und Versionscheck |
| `git diff --check` | PASS | generiertes Minified-Bundle gezielt ausgenommen |
| Workflow-YAML-Lint | NOT RUN | PyYAML, Ruby, actionlint und vergleichbare Parser fehlen lokal |
| Home-Assistant 2026.10.1-Fixture | BLOCKED | kein Docker/Podman/pip/ensurepip; venv-Erstellung scheitert an fehlendem ensurepip |
| Config-/Options-Flow in HA | BLOCKED | HA-Core nicht installiert |
| Coordinator/Reload/Unload in HA | BLOCKED | HA-Fixture nicht verfügbar |
| Frontend-Ressourcenregistrierung in HA | BLOCKED | HA-Fixture nicht verfügbar |
| Hassfest | BLOCKED | nur lokaler Workflow vorhanden; kein HA-Action-Runner |
| HACS-Validator | BLOCKED | kein HACS-Validator/CI-Runner lokal |
| Gitleaks | NOT RUN | Binary nicht installiert |
| GitHub Actions auf diesem Kandidaten | NOT RUN | Branch nicht gepusht; Dispatch wäre externe Aktion und nicht autorisiert |
| Produktive HA-Installation/Dashboard | NOT RUN | ausdrücklich ausgeschlossen |

## Isolierte Testumgebung

Geprüft wurden Docker, Podman, `uv`, `pytest`, `act` und Gitleaks; keines dieser
Werkzeuge ist verfügbar. Ein temporärer Python-venv-Versuch scheiterte mit dem
konkreten Fehler, dass `ensurepip` nicht verfügbar ist. Es wurden dabei keine
Systempakete und keine Pakete in Home Assistant installiert.

Die vorhandenen GitHub-Workflows installieren HA 2026.10.1, pytest,
pytest-asyncio und `pytest-homeassistant-custom-component` ausschließlich auf
GitHub-Runnern. Sie wurden lokal statisch geprüft, aber für diesen nicht
veröffentlichten Branch nicht ausgeführt.

## Integrations- und Migrationsteststatus

Offline abgesichert sind:

- interne Domain `air_traffic_merge`
- Config-Entry-Schlüssel und bestehende Unique-ID-Verträge
- FR24-, ADS-B-URL- und ADS-B-Entity-Datenverträge
- Deduplizierung, ungültige Koordinaten und veraltete Positionen
- alte Sensorattribute und Tracking-Event
- neue und Legacy-Kartenregistrierung
- Legacy-Parameter einschließlich `max_items: 25`
- Bundle-Build und Versionsmarker

Nicht tatsächlich in Home Assistant ausgeführt sind Installation, Config Flow,
Options Flow, Sensor-/Binary-Sensor-Lebenszyklus, Reload, Unload, automatische
Lovelace-Ressourcenregistrierung und eine echte Registry-Migration. Deshalb
wird keine vollständige HA-Laufzeitkompatibilität behauptet.

Live-API-Tests wurden nicht ausgeführt. Es liegen keine Zugangsdaten vor und
die Offline-Fixtures sind für die Quellverträge ausreichend, ohne externe APIs
oder deren Rate-Limits zu belasten.

## Workflow- und Releaseprüfung

Die vorbereiteten Workflows verwenden GitHub-hosted Runner, pinnen die
Home-Assistant-Testversion auf `2026.10.1`, prüfen den generierten Bundle-Diff
und führen Secret-Scanning in einem separaten Job aus. Der Release-Workflow ist
nur per `workflow_dispatch` mit einem vorhandenen Tag auslösbar und wurde nicht
ausgeführt.

Die alte Remote-Integration besitzt derzeit nur den bestehenden Validate-
Workflow; historische Validate-Läufe auf dem alten Remote waren erfolgreich.
Das beweist nicht die Ausführung der neuen lokalen Phase-6-Workflows.

Die vorgeschlagene Beta-Version `1.4.0-beta.1` ist aufgrund des konsolidierten
Frontend-/Backend-Kandidaten und der bereits vorhandenen Manifest-/Paketversion
plausibel. Sie ist noch kein Release und kein Tag.

## Repository-Umbenennung

Vorbereitet und dokumentiert, nicht durchgeführt:

- künftiges Ziel `balronu/ha-air-traffic` bleibt derzeit 404
- bestehendes Remote bleibt `balronu/air-traffic-merge`
- technische Domain bleibt `air_traffic_merge`
- README-, Manifest-, Issue- und Workflow-Zielwerte zeigen auf die künftige
  Adresse, ohne eine Remote-Änderung auszulösen
- GitHub-Redirects und HACS-Risiken sind in
  `docs/PHASE4-MIGRATION.md` dokumentiert
- Kartenrepository wurde nicht archiviert

Rollback bleibt über die unveränderte technische Domain, bestehende Legacy-
Karte und alte Lovelace-Ressource vorgesehen.

## Verbleibende Risiken

1. Home-Assistant-API-/Manifestabweichungen können erst durch Hassfest und eine
   echte HA-Fixture ausgeschlossen werden.
2. Registry-, Geräte-, Config-Entry- und Reload-/Unload-Verhalten ist nur als
   Offline-Vertrag abgesichert.
3. HACS-Installation und Release-Artefakte sind noch nicht remote validiert.
4. Secret-Scanning wurde nicht ausgeführt.
5. Echte Desktop-/Mobil-/Detail-/Konfigurationsscreenshots fehlen weiterhin.

## Nächste Schritte vor Beta-Freigabe

1. Exakten Branch in einen isolierten CI-Runner bringen, ohne zu veröffentlichen
   oder zu mergen.
2. HA-Fixture mit HA 2026.10.1, Hassfest, HACS-Validierung und Gitleaks
   erfolgreich ausführen.
3. Config-/Options-Flow sowie Reload/Unload und Frontend-Ressourcenregistrierung
   in dieser Fixture testen.
4. Erst danach eine Beta-Freigabe, Tag, Release oder Repository-Umbenennung
   separat autorisieren.

Phase 6 endet damit bei **NOT READY FOR BETA**. Phase 7 wurde nicht begonnen.
