# Air Traffic – Phase 5 Abschlussbericht

**Branch:** `work/air-traffic-modernization`  
**Ausgangscommit:** `e9deae4c2b6bcb70e44cae40f6b732594a3b33c0`  
**Implementation-Commit:** wird nach dem lokalen Commit eingetragen  
**Git-Status:** wird nach dem lokalen Commit abschließend geprüft  
**Phase 6:** nicht begonnen

## Branding und Bilder

Das Projektbranding verwendet öffentlich ausschließlich **Air Traffic**. Die
technische Domain `air_traffic_merge` bleibt unverändert.

Erstellt und geprüft:

| Datei | Abmessung | Ergebnis |
|---|---:|---|
| `images/branding/air-traffic-logo.png` | 1024 × 1024 RGBA | PASS |
| `images/branding/air-traffic-social-preview.png` | 1280 × 640 RGB | PASS |
| `images/branding/air-traffic-readme-banner.png` | 1600 × 533 RGB | PASS |
| `images/branding/air-traffic-banner-background.png` | 2172 × 724 RGB | PASS, Roh-/Quellasset |

Logo, Social Preview und Banner wurden mit dem verfügbaren Bildgenerator als
visuelle Projektassets erstellt. Bannertexte wurden anschließend deterministisch
gesetzt. Es wurden keine simulierten Home-Assistant-Oberflächen als Screenshots
ausgegeben.

Echte Desktop-, Mobil-, Flugzeugdetail- und Konfigurationsscreenshots sind
`NOT RUN / NOT AVAILABLE`, weil keine isolierte oder produktive HA-Frontend-
Umgebung zur Verfügung stand. Das ist in beiden READMEs ausdrücklich vermerkt.

## Dokumentation

- `README.md` vollständig auf Englisch überarbeitet
- `README.de.md` inhaltlich entsprechend auf Deutsch überarbeitet
- Inhaltsverzeichnisse, Datenquellen, Installation, Konfiguration, Kartenoptionen,
  Migration, Datenschutz, Fehlerbehebung und bekannte Einschränkungen ergänzt
- Branding in beide READMEs eingebunden
- `CONTRIBUTING.md` ergänzt
- `CHANGELOG.md` und Entwurf `docs/releases/RELEASE_NOTES_v1.4.0-beta.1.md`
  ergänzt
- `docs/BRANDING.md` und `docs/GITHUB-PREPARED.md` ergänzt

## GitHub-Vorbereitung

Lokal vorbereitet:

- Issue-Formulare für Bug, Feature und Support
- Issue-Konfiguration mit zukünftigem Ziel-Link
- Pull-Request-Vorlage
- Release-Kategorien und manuell ausgelöster Release-Workflow
- bestehende Test-/Validate-Workflows weiterverwendet
- Zielbeschreibung und Topic-Vorschläge dokumentiert
- HACS-Anzeige `Air Traffic` und MIT-Lizenz beibehalten

Nicht durchgeführt:

- kein Push oder Merge
- kein Repository erstellt oder umbenannt
- keine Remote-Beschreibung oder Topics gesetzt
- kein GitHub-Social-Preview hochgeladen
- kein Release und kein Tag
- Kartenrepository nicht archiviert

## Versionsstrategie

Die vorgeschlagene erste gemeinsame Entwicklungsversion ist
`1.4.0-beta.1`. Diese Version war bereits im Manifest, im Frontend-Paket und in
der versionierten Bundle-URL vorhanden. Sie bezeichnet den konsolidierten
Beta-Kandidaten und ist kein veröffentlichter Release.

## Testergebnisse

| Prüfung | Status | Nachweis |
|---|---|---|
| Python-/Migrations-Tests | PASS | 14/14 unittest |
| Frontend-Tests | PASS | 3/3 Vitest |
| Frontend-Build | PASS | TypeScript/Vite |
| Bundle-Syntax | PASS | `node --check` |
| Python Compileall | PASS | lokale Python-Laufzeit |
| JSON-Validierung | PASS | alle Projekt-JSON-Dateien |
| Bilddateien/Abmessungen | PASS | Pillow-Prüfung |
| Lokale Markdown-Links | PASS | README und README.de |
| `git diff --check` | PASS | generiertes Minified-Bundle ausgenommen |
| Workflow-YAML-Lint | BLOCKED | PyYAML lokal nicht installiert |
| Hassfest | BLOCKED | nur CI-Workflow vorbereitet |
| HACS-Validierung | BLOCKED | nur CI-Workflow vorbereitet |
| Home-Assistant-Fixture | BLOCKED | lokale HA-/pip-/venv-Tools fehlen |
| Gitleaks | NOT RUN | Binary lokal nicht verfügbar |
| Echte HA-Screenshots | NOT RUN | keine HA-Frontend-Umgebung |

## Offene Punkte und nächste Freigaben

Vor einer Veröffentlichung müssen die CI-Gates auf dem exakten Branch bestehen.
Danach sind Repository-Umbenennung, Remote-Metadaten, Social Preview, Release,
Migration des alten Kartenrepositories und dessen Archivierung jeweils separat
freizugeben. Phase 6 wurde nicht begonnen.
