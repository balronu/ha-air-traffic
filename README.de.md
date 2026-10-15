<p align="center">
  <img src="images/branding/air-traffic-logo.png" alt="Air Traffic Logo" width="180">
</p>

<p align="center">
  <img src="images/branding/air-traffic-readme-banner.png" alt="Air Traffic – Home-Assistant-Integration mit integrierter Lovelace-Karte">
</p>

# Air Traffic

Air Traffic ist eine Home-Assistant-Integration, die einen vorhandenen
Flightradar24-Sensor mit lokalen ADS-B-Daten zusammenführt und die Lovelace-
Karte im selben Integrations-Bundle mitliefert.

> **Status:** lokaler Entwicklungsstand auf
> `work/air-traffic-modernization`. Das zukünftige Repository
> `balronu/ha-air-traffic` wurde noch nicht erstellt oder umbenannt.

## Inhalt

- [Funktionen](#funktionen)
- [Unterstützte Datenquellen](#unterstützte-datenquellen)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Lovelace-Karte](#lovelace-karte)
- [Migration von Air Traffic Merge](#migration-von-air-traffic-merge)
- [Aktualisierung](#aktualisierung)
- [Fehlerbehebung](#fehlerbehebung)
- [Datenschutz und Datenquellen](#datenschutz-und-datenquellen)
- [Bekannte Einschränkungen](#bekannte-einschränkungen)
- [Screenshots](#screenshots)
- [Mitwirkung und Support](#mitwirkung-und-support)
- [Lizenz](#lizenz)

## Funktionen

- Nur FR24, nur ADS-B oder kombinierter Quellmodus
- ADS-B-Daten über URL mit `aircraft.json` oder über eine bestehende Entity
- Normalisierung, Zusammenführung und Unterdrückung von Duplikaten
- Tracking nach Callsign, Registrierung oder beidem
- Gemeinsamer `DataUpdateCoordinator` mit Wiederholungen und Quellfehlern
- Responsive Lovelace-Karte mit Lade-, Fehler- und Stale-Zuständen
- Flugzeugauswahl, Detailansicht sowie helle/dunkle Theme-Variablen
- Kompatibilität mit `custom:air-traffic-merge-card`

## Unterstützte Datenquellen

### Flightradar24-Entity

Der ausgewählte Sensor muss in seinen Attributen eine Liste `flights`
bereitstellen. Air Traffic ruft keine FR24-API auf und verarbeitet keine
FR24-Zugangsdaten.

### ADS-B-URL

Die URL muss JSON mit einer Liste `aircraft` liefern, zum Beispiel ein lokaler
`readsb`-/`tar1090`-Endpunkt. Bei einer Host-URL ergänzt die Integration
`/data/aircraft.json`.

### ADS-B-Entity

Der ausgewählte Sensor muss eine Liste `aircraft` liefern. `messages` und `now`
werden übernommen, wenn die Quelle sie bereitstellt. Fehlende Werte werden nicht
erfunden.

## Voraussetzungen

- Aktuelle, zur installierten Version passende Home-Assistant-Version
- HACS oder Möglichkeit zur manuellen Installation
- Mindestens eine unterstützte Datenquelle
- Netzwerkzugriff von Home Assistant auf den ADS-B-Endpunkt im URL-Modus

## Installation

### HACS

Die geplante Quelle ist `balronu/ha-air-traffic`. Sie ist noch nicht
veröffentlicht. Nach ausdrücklicher Freigabe in **HACS → Integrationen** nach
**Air Traffic** suchen, installieren, Home Assistant neu starten und die
Integration unter **Einstellungen → Geräte & Dienste** hinzufügen.

Die zukünftige URL darf vor ihrer Veröffentlichung nicht installiert werden.

### Manuelle Installation

Das Verzeichnis `custom_components/air_traffic_merge` nach
`/config/custom_components/` kopieren und Home Assistant neu starten. Der
Verzeichnisname bleibt als technischer Kompatibilitäts-Identifier erhalten.

## Konfiguration

Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** **Air
Traffic** auswählen. Der Flow bietet FR24, ADS-B oder beide Quellen, die
Entity-/URL-Auswahl, das Abfrageintervall und optionales Tracking.

Die interne Domain bleibt `air_traffic_merge`; Config Entries, Entities, Unique
IDs und Optionen werden nicht umbenannt.

## Lovelace-Karte

Die Integration stellt das versionierte Frontend automatisch bereit. Ein zweites
Kartenrepository ist nicht erforderlich.

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

Bestehende Dashboards dürfen weiterhin den Legacy-Typ verwenden:

```yaml
type: custom:air-traffic-merge-card
entity: sensor.air_traffic_merged
```

Beide Typen verwenden dieselbe aktuelle Implementierung. Dashboards und
`.storage/lovelace.resources` werden nicht geändert. Die Bundle-URL lautet:

```text
/air_traffic_merge/air-traffic-card.js?v=1.4.0-beta.1
```

### Kartenoptionen

| Option | Standard | Beschreibung |
|---|---:|---|
| `entity` | erforderlich | Zusammengeführte Entity |
| `title` | `Air Traffic` | Überschrift |
| `show_status` | `true` | Quell- und Zusammenführungszähler |
| `show_debug` | `false` | Rohe Attribute zur Diagnose |
| `show_counts` | `false` | Kategorienzählung, falls vorhanden |
| `max_items` | `25` | Maximal angezeigte Flüge |
| `compact` | `false` | Hinweis für kompakte Kartenhöhe |

## Migration von Air Traffic Merge

Der öffentliche Name wird **Air Traffic**, die interne Domain bleibt jedoch
`air_traffic_merge`. Die Integration darf wegen der öffentlichen
Repository-Umbenennung nicht gelöscht und neu angelegt werden.

Der Legacy-Typ `custom:air-traffic-merge-card` bleibt registriert. Nach Prüfung
des neuen Bundles kann in einer Dashboard-Kopie auf
`custom:air-traffic-card` gewechselt werden. Vorhandene Ressourcen werden nicht
automatisch gelöscht. Siehe den [Phase-4-Migrationsleitfaden](docs/PHASE4-MIGRATION.md).

## Aktualisierung

Vorher ein Home-Assistant-Backup erstellen. Danach die zentrale Entity, die
Karte und den Quellstatus prüfen. Die Bundle-URL enthält eine Versionsabfrage.
Aus diesem lokalen Kandidaten wurde noch kein Release veröffentlicht.

## Fehlerbehebung

- **Keine Flüge:** Entity und Liste `flights`/`aircraft` prüfen.
- **ADS-B-URL-Fehler:** Endpunkt vom HA-Host öffnen und JSON mit `aircraft`
  prüfen.
- **Veraltete Daten:** `data_stale` und `source_errors` prüfen.
- **Karte nicht gefunden:** Frontend neu laden und alte Ressource erst danach
  entfernen.
- **Fehlende Attribute:** Quellformate unterscheiden sich; Werte bleiben leer.

## Datenschutz und Datenquellen

Air Traffic verarbeitet Daten der konfigurierten Entity oder des ADS-B-Endpunkts.
Es gibt keine integrierte Cloud-Anmeldung und keine Weiterleitung von FR24-
Zugangsdaten. Lokale Aufrufe unterliegen den Bedingungen und Rate-Limits der
jeweiligen Quelle.

## Bekannte Einschränkungen

- Die Karte ist eine responsive Flugzeugliste mit Detailansicht, keine
  geografische Karte mit Zoom-Engine.
- HA-Fixture sowie Hassfest- und HACS-Validierung waren lokal nicht verfügbar
  und bleiben Release-Gates.
- Der genaue Feldumfang hängt von der Datenquelle ab.

## Screenshots

Es sind noch keine Screenshots als Funktionsnachweis enthalten. Eine produktive
oder isolierte HA-Testumgebung stand nicht zur Verfügung. Generierte oder
simulierte Oberflächen werden nicht als echte Funktionen ausgegeben. Die
Branding-Assets in `images/branding/` sind nur Projektgrafiken.

## Mitwirkung und Support

Vor Issue oder Pull Request bitte [CONTRIBUTING.md](CONTRIBUTING.md) lesen.
Home-Assistant-Version, Integrationsversion, Quellmodus und anonymisierte
Fehlerdaten angeben. Niemals Schlüssel, Tokens, private URLs oder persönliche
Standortdaten veröffentlichen.

## Lizenz

Air Traffic steht unter der [MIT-Lizenz](LICENSE).
