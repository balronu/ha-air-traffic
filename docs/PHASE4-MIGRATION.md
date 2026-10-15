# Air Traffic – Phase 4: Migration und Rückwärtskompatibilität

**Branch:** `work/air-traffic-modernization`  
**Ausgangscommit:** `8e91e302b9fdcee6fcf3d2537b9f717336b4ec6c`  
**Interne Domain:** `air_traffic_merge`  
**Öffentlicher Name:** Air Traffic

Dieses Dokument beschreibt die lokale Kandidatenimplementierung. Es wurden
weder eine produktive Home-Assistant-Installation noch ein GitHub-Repository,
ein Dashboard oder eine Lovelace-Ressourcendatei verändert.

## Kompatibilitätsmatrix

| Vertrag | Bisheriger Stand | Phase-4-Stand | Bewertung |
|---|---|---|---|
| HA-Domain | `air_traffic_merge` | unverändert | PASS, keine Domainmigration |
| Config-Flow-Version | `1` | `1` | PASS, kein automatischer Entry-Migrationsschritt |
| Config-Entry-Daten | `source_mode`, `fr24_entity`, `adsb_source`, `adsb_url`, `adsb_entity`, `scan_interval`, `enable_tracking`, `track_mode`, `track_callsigns`, `track_registrations` | gleiche Schlüssel | PASS als Quelltextvertrag; echte HA-Registry BLOCKED |
| Config-Entry-/Options-Schema | bestehende Quellmodi und Trackingoptionen | gleiche Modi und Schlüssel | PASS offline; HA-Flow-Fixture BLOCKED |
| Hauptentität | `sensor.air_traffic_merged` | unverändert | PASS im Quelltextvertrag |
| Hauptentität Unique ID | `<entry_id>_merged` | unverändert | PASS im Quelltextvertrag |
| Tracking-Zähler | `sensor.air_traffic_tracked_count`, `<entry_id>_tracked_count` | unverändert | PASS im Quelltextvertrag |
| Tracking-Binary-Sensor | `binary_sensor.air_traffic_tracked_present`, `<entry_id>_tracked_present` | unverändert | PASS im Quelltextvertrag |
| Alte Sensorattribute | `last_update`, `flights`, `aircraft`, `messages`, `now` sowie Tracking-/Zählwerte | alle erhalten; Fehler-/Stale-Attribute ergänzt | PASS offline |
| Tracking-Event | `air_traffic_merge_tracked` | unverändert | PASS im Quelltextvertrag; HA-Ereignis-Fixture BLOCKED |
| FR24-Quelle | Sensorattribut `flights` | weiterhin gelesen | PASS offline; reale HA-Entity NOT RUN |
| ADS-B-Entity | Sensorattribut `aircraft` | weiterhin gelesen | PASS offline; reale HA-Entity NOT RUN |
| ADS-B-URL | JSON mit `aircraft` | weiterhin gelesen, normalisiert und retried | PASS offline; externe API NOT RUN |
| Legacy-Karte | `custom:air-traffic-merge-card` | Alias auf dieselbe aktuelle Implementierung | PASS Bundle-/Frontend-Test |
| Neue Karte | nicht vorhanden | `custom:air-traffic-card` | PASS Bundle-/Frontend-Test |
| Kartenparameter | `entity`, `title`, `show_status`, `show_debug`, `show_counts`, `max_items`, `compact` | alle akzeptiert; Default `max_items: 25` bleibt erhalten | PASS Frontend-Test |
| Alte Ressourcen-URL | typischerweise `/hacsfiles/air-traffic-merge-card/dist/air-traffic-merge-card.js` | wird nicht automatisch gelöscht | PASS Sicherheitsentscheidung |
| Neue Ressourcen-URL | nicht vorhanden | `/air_traffic_merge/air-traffic-card.js?v=1.4.0-beta.1` automatisch | PASS als Setup-/Bundlevertrag; HA-Fixture BLOCKED |
| Dashboards/Automationen | außerhalb der Repositories | nicht geschrieben oder umbenannt | PASS: keine automatische Änderung |
| Entity Registry/Geräte | nur in produktiver HA-Instanz vorhanden | nicht angerührt | NOT RUN, produktive Prüfung ausdrücklich ausgeschlossen |

### Was diese Matrix nicht beweist

Ohne eine Home-Assistant-Test-Fixture mit einer gespeicherten Config Entry und
Entity Registry kann kein lokaler Test behaupten, dass eine konkrete Registry
oder ein konkretes Geräte-Mapping unverändert bleibt. Das wird deshalb als
`BLOCKED` beziehungsweise `NOT RUN` ausgewiesen und nicht durch einen
Quelltextvergleich ersetzt.

## Migrationsstrategie

Die sichere Strategie ist eine **öffentliche Umbenennung bei unveränderter
technischer Identität**:

1. Die bestehende Domain `air_traffic_merge` bleibt im Integrationspfad und im
   Manifest erhalten.
2. Config Entries, Entity IDs, Unique IDs und gespeicherte Optionen werden nicht
   neu angelegt, kopiert oder automatisch umbenannt.
3. Die Karte wird aus demselben versionierten Bundle bereitgestellt. Das Bundle
   registriert beide Custom-Element-Namen idempotent.
4. Die Legacy-Ressource und Legacy-Karte werden nicht aus Dashboards entfernt.
   Nutzer können nach erfolgreicher Prüfung manuell auf den neuen Kartentyp
   wechseln.
5. Eine spätere Domainmigration ist ein separates Projekt und darf erst nach
   einer echten HA-Fixture mit Registry-/Entry-Import getestet werden.

### Automatisch durch die Integration

- Statischer Pfad `/air_traffic_merge/` wird bereitgestellt.
- Die versionierte Bundle-URL wird genau einmal über `add_extra_js_url`
  registriert.
- `air-traffic-card` und `air-traffic-merge-card` werden nur registriert, wenn
  der jeweilige Custom-Element-Name noch nicht vorhanden ist.
- Doppelte `window.customCards`-Einträge werden vermieden.
- Coordinator- und Plattformdaten werden beim Reload freigegeben.

### Bewusst manuelle Schritte

Nach einem später freigegebenen Release:

1. Vorher ein HA-Backup erstellen.
2. Neue Integration aus der freigegebenen Quelle installieren/aktualisieren.
3. Prüfen, dass `sensor.air_traffic_merged` und die übrigen bisherigen
   Entitäten dieselben Entity IDs und Werte liefern.
4. Ein bestehendes Dashboard unverändert öffnen und die Legacy-Karte prüfen.
5. Optional den Kartentyp in einer Kopie des Dashboards von
   `custom:air-traffic-merge-card` auf `custom:air-traffic-card` ändern.
6. Erst danach die alte Karten-Ressource und das alte Karten-Repository manuell
   entfernen. Die Integration nimmt diese Löschung nicht vor.

## Karten- und Dashboard-Kompatibilität

Die Legacy-Klasse ist eine eigene Unterklasse der aktuellen
`AirTrafficCard`. Dadurch kann der Browser beide Custom-Elemente registrieren,
ohne denselben Konstruktor unter zwei Namen zu definieren. Beide Typen nutzen
dieselben Rendering-, Zustands- und Detailansichten.

Explizit erhaltene Legacy-Optionen:

```yaml
type: custom:air-traffic-merge-card
entity: sensor.air_traffic_merged
title: Air Traffic
show_status: true
show_debug: false
show_counts: true
max_items: 25
compact: false
```

Die Karte schreibt weder YAML noch `.storage/lovelace.resources`. Eine alte
manuell eingetragene Ressource bleibt daher zunächst bestehen. Sie darf erst
nach einer erfolgreichen Prüfung entfernt werden, damit kein Dashboard durch
die Migration unbrauchbar wird.

## HACS-Migration und Repository-Umbenennung

Derzeit existiert lokal der Branch im Repository
`balronu/air-traffic-merge`; das Ziel `balronu/ha-air-traffic` wurde nicht
erstellt. Beide alten GitHub-Repositories bleiben unverändert.

GitHub dokumentiert, dass eine Repository-Umbenennung Web- und Git-Weiterleitungen
bereitstellt und alte Clone-/Fetch-/Push-URLs zunächst weiter funktionieren.
GitHub weist zugleich darauf hin, dass Referenzen in GitHub Actions nicht
automatisch weitergeleitet werden können. Siehe die [offizielle GitHub-
Dokumentation zur Repository-Umbenennung](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).

Das ist **keine belastbare Zusage**, dass HACS jede vorhandene Custom-Repository-
Referenz, ihren Cache und jede Frontend-Ressource automatisch auf einen neuen
Slug umstellt. Eine HACS-Live-Instanz wurde in Phase 4 nicht ausgeführt.

Empfohlene Reihenfolge nach separater Freigabe:

1. Einen getesteten Release im neuen Zielrepository veröffentlichen und dessen
   HACS-Metadaten/Build-Artefakte prüfen.
2. Die alte Integrationsquelle mit einem deutlichen Migrationshinweis und einem
   letzten kompatiblen Stand bestehen lassen.
3. Nutzer informieren, dass die technische Domain nicht geändert wird und keine
   Config Entry neu angelegt werden soll.
4. Die neue Bundle-URL nach einem HA-Neustart prüfen.
5. Erst nach beobachteter erfolgreicher Migration das alte Kartenrepository
   beziehungsweise alte Ressourcen aus den jeweiligen Installationen entfernen.

Eine automatische Repository-Umbenennung, Archivierung oder Release-Erstellung
ist nicht Bestandteil dieses Branches.

## Rollback

Bei einem Fehler:

1. HA-Backup oder den vorherigen Integrationsstand wiederherstellen.
2. Die bestehende Config Entry und Entity Registry nicht löschen.
3. Das unveränderte alte Karten-Bundle als Lovelace-Ressource wieder aktivieren,
   falls die neue Ressource nicht lädt.
4. Das Dashboard auf `custom:air-traffic-merge-card` belassen.
5. Erst nach Logprüfung und einem reproduzierbaren Fix erneut testen.

Da Phase 4 weder Domain noch Config Entries umbenennt und keine Dashboards
schreibt, ist der vorgesehene Rollback ohne automatische Registry-Bereinigung
möglich.

## Reproduzierbare lokale Migrationstests

Die Tests liegen in `tests/test_migration_contract.py` und
`frontend/tests/air-traffic-card.test.ts`. Sie prüfen die unveränderten
technischen Schlüssel/IDs, Attribute, Event- und Kartennamen sowie die
idempotente Legacy-/Neue-Kartenregistrierung. Die Bundle-Synchronität wird im
CI-Workflow geprüft.

Eine echte HA-Fixture mit `.storage/core.config_entries`, Entity Registry,
Geräteregistry und Reload/Unload konnte wegen der fehlenden lokalen
Python-/HA-Testumgebung nicht ausgeführt werden. Dafür sind die CI-Gates in
`.github/workflows/tests.yml` und `.github/workflows/validate.yml` vorbereitet.

## Testergebnisse

| Test | Ergebnis |
|---|---|
| Offline-Kompatibilitätsverträge | PASS |
| Legacy-/neuer Frontend-Kartentyp | PASS |
| Legacy-Parameter einschließlich `max_items: 25` | PASS |
| Frontend-Build und Bundle-Synchronität | PASS, nach aktuellem Build erneut zu bestätigen |
| HA Config-Entry-/Registry-Fixture | BLOCKED: kein lokales HA-/pip-/venv-Tooling |
| Reload/Unload in HA | BLOCKED: kein HA-Fixture |
| Hassfest | BLOCKED: CI vorbereitet, lokal nicht verfügbar |
| HACS-Validierung | BLOCKED: CI vorbereitet, lokal nicht verfügbar |
| Gitleaks | NOT RUN: Binary lokal nicht verfügbar |
| Produktive HA-/Dashboard-Migration | NOT RUN: ausdrücklich ausgeschlossen |

