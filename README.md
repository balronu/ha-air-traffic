<p align="center">
  <img src="images/branding/air-traffic-logo.png" alt="Air-Traffic-Logo" width="160">
</p>

<p align="center">
  <img src="images/branding/air-traffic-readme-banner.png" alt="Air Traffic – Home-Assistant-Integration mit integrierter Lovelace-Karte">
</p>

<p align="center">🇩🇪 Deutsch | <a href="README.md">🇬🇧 English</a></p>

# Air Traffic

Air Traffic ist eine benutzerdefinierte Home-Assistant-Integration, die einen
Flightradar24-Sensor mit lokalen ADS-B-Daten zusammenführt. Beide Quellen
werden normalisiert und doppelte Flugzeuge unterdrückt. Die Integration stellt
stabile Home-Assistant-Entities bereit und liefert die responsive Lovelace-
Karte im selben Integrationspaket.

> **Release-Status:** Die zuletzt veröffentlichte stabile Version ist `v1.3.1`.
> `1.4.0-beta.1` ist vorbereitet, aber noch nicht veröffentlicht. Die isolierte
> Lovelace-Browserprüfung ist noch offen; diese README stellt die
> unveröffentlichte Beta nicht als allgemein verfügbar dar.

## Inhalt

- [Funktionen](#funktionen)
- [Unterstützte Quellen](#unterstützte-quellen)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Entities und Attribute](#entities-und-attribute)
- [Lovelace-Karte](#lovelace-karte)
- [Migration](#migration)
- [Aktualisierung](#aktualisierung)
- [Fehlerbehebung](#fehlerbehebung)
- [Datenschutz und Einschränkungen](#datenschutz-und-einschränkungen)
- [Mitwirkung](#mitwirkung)
- [Lizenz](#lizenz)

## Funktionen

- Nur FR24, nur ADS-B oder kombinierter Quellenmodus
- ADS-B über eine URL mit `aircraft.json`
- ADS-B über eine vorhandene Home-Assistant-Entity mit Attribut `aircraft`
- Normalisierung, Duplikaterkennung und Quellen-Zusammenführung
- Optionales Tracking nach Callsign, Registrierung oder beidem
- Gemeinsamer `DataUpdateCoordinator` mit Wiederholungen für ADS-B-URLs
- Ungültige Koordinaten und veraltete ADS-B-Positionen werden sicher behandelt
- Integrierte responsive Karte mit Leer-, Fehler-, Nichtverfügbar- und Stale-Zuständen
- Flugzeugauswahl und Detailansicht
- Neuer und Legacy-Lovelace-Elementname im selben Bundle

## Unterstützte Quellen

| Quelle | Erforderliche Daten | Hinweise |
|---|---|---|
| Flightradar24-Entity | Sensorattribut `flights` als Liste | Air Traffic ruft keine FR24-API auf und verwaltet keine FR24-Zugangsdaten. |
| ADS-B-URL | JSON-Objekt mit einer Liste `aircraft` | Bei einer Host-URL wird `/data/aircraft.json` ergänzt; HTTP-Fehler und Timeouts werden wiederholt. |
| ADS-B-Entity | Sensorattribut `aircraft` als Liste | Die optionalen Attribute `messages` und `now` werden übernommen. |

Die Integration versteht gängige Feldnamen von FR24/readsb/tar1090 und
normalisiert, soweit vorhanden, Callsign, Registrierung, ICAO/Hex, Höhe,
Geschwindigkeit, Kurs, Koordinaten, Entfernung, Kategorie, Squawk und
Positionsalter. Fehlende Werte werden nicht erfunden.

## Voraussetzungen

- Home Assistant mit aktivierten benutzerdefinierten Integrationen
- HACS oder die Möglichkeit zur manuellen Installation
- Mindestens eine unterstützte Quelle
- Netzwerkzugriff von Home Assistant auf die ADS-B-URL im URL-Modus

Für normale Installationen sollte die veröffentlichte stabile Version verwendet
werden. `main` und `1.4.0-beta.1` sind Entwicklungskandidaten, solange die
Beta-Prüfungen nicht abgeschlossen sind.

## Installation

### HACS

1. **HACS → Integrationen** öffnen.
2. Nach **Air Traffic** suchen oder das Repository
   [`balronu/ha-air-traffic`](https://github.com/balronu/ha-air-traffic) als
   benutzerdefiniertes Repository vom Typ **Integration** hinzufügen.
3. Die zuletzt veröffentlichte Version installieren.
4. Home Assistant neu starten.
5. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** **Air
   Traffic** hinzufügen.

Das öffentliche Repository wurde von `air-traffic-merge` in `ha-air-traffic`
umbenannt. Die technische Home-Assistant-Domain und das Integrationsverzeichnis
bleiben aus Kompatibilitätsgründen `air_traffic_merge`. Eine bestehende
Installation sollte aktualisiert und nicht nur wegen des Repository-Namens
gelöscht und neu angelegt werden.

### Manuelle Installation

`custom_components/air_traffic_merge` nach
`/config/custom_components/air_traffic_merge/` kopieren und Home Assistant neu
starten. Für veröffentlichte Versionen wird HACS empfohlen.

## Konfiguration

Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** **Air
Traffic** auswählen und einen Quellenmodus wählen:

| Flow-Schritt | Verfügbare Einstellungen |
|---|---|
| Quelle | Nur FR24, nur ADS-B oder beide; Tracking an/aus |
| FR24-Sensor | Sensor-Entity mit dem Attribut `flights` |
| ADS-B-Quelle | URL (`aircraft.json`) oder bestehende Sensor-Entity |
| ADS-B-URL | URL; bei Host-URLs wird `/data/aircraft.json` ergänzt |
| ADS-B-Entity | Sensor-Entity mit dem Attribut `aircraft` |
| Tracking-Modus | Callsign, Registrierung oder beides |
| Tracking-Werte | Kommagetrennte Callsigns und/oder Registrierungen |

Bei ADS-B-Quellen beträgt das Mindestintervall fünf Sekunden, standardmäßig
sind es zehn Sekunden. Der Options Flow ändert Intervall und Tracking. Wenn
Tracking aktiviert ist, werden dort zusätzlich Modus und Werte angezeigt.

## Entities und Attribute

Die Entity IDs werden normalerweise aus den Entity-Namen gebildet. Bestehende
IDs und Unique IDs sind Teil des Kompatibilitätsvertrags und dürfen nicht
umbenannt werden.

| Entity | Zweck |
|---|---|
| `sensor.air_traffic_merged` | Anzahl zusammengeführter Flugzeuge und vollständiger normalisierter Snapshot |
| `sensor.air_traffic_tracked_count` | Anzahl aktuell verfolgter Flugzeuge |
| `binary_sensor.air_traffic_tracked_present` | Ein, solange mindestens ein verfolgtes Flugzeug vorhanden ist |

Der zusammengeführte Sensor besitzt die Attribute:

`last_update`, `flights`, `aircraft`, `messages`, `now`, `fr24_count`,
`adsb_count`, `merged_count`, `tracking_enabled`, `tracked_active_count`,
`matched_callsigns`, `matched_registrations`, `source_errors` und `data_stale`.

Jedes normalisierte Element in `flights` kann `key`, `registration`, `hex`,
`callsign`, `source`, `aircraft_model`, `airline`, `alt_m`, `spd_kmh`,
`dist_km`, `dir_deg`, `latitude`, `longitude`, `position_age_s`,
`position_stale`, `category`, `squawk`, `tracked`, `tracked_by` und
`tracked_target` enthalten. Welche Felder vorhanden sind, hängt von der Quelle
ab.

Der Tracking-Zähler und der Binary-Sensor liefern zusätzlich Trackingstatus und
getroffene Callsigns/Registrierungen. Bei einem Quellfehler bleiben die letzten
Quelldaten erhalten, `source_errors` wird gesetzt und `data_stale` wird `true`.

## Lovelace-Karte

Die Integration stellt ihr versioniertes Bundle automatisch bereit und
registriert es. Bei einer neuen Installation ist kein separates Karten-
Repository und keine manuelle Ressource nötig:

```yaml
type: custom:air-traffic-card
entity: sensor.air_traffic_merged
title: Air Traffic
show_status: true
show_debug: false
show_counts: false
max_items: 25
compact: false
```

Bestehende Dashboards dürfen den kompatiblen Legacy-Namen behalten:

```yaml
type: custom:air-traffic-merge-card
entity: sensor.air_traffic_merged
title: Air Traffic
max_items: 25
```

Beide Namen verwenden dieselbe Implementierung. Die Karte zeigt Quellzähler,
Flugzeugzeilen, normalisierte Werte, Stale-/Fehlerzustände und eine auswählbare
Detailansicht. Auf schmalen Karten wechselt das Layout von vier auf zwei
Metrikspalten. Für helle und dunkle Themes werden Home-Assistant-Variablen
verwendet.

### Kartenoptionen

| Option | Standard | Bedeutung |
|---|---:|---|
| `entity` | erforderlich | Entity, deren Attribut `flights` angezeigt wird |
| `title` | `Air Traffic` | Überschrift |
| `show_status` | `true` | FR24-, ADS-B- und Zusammenführungszähler anzeigen |
| `show_debug` | `false` | Rohe Entity-Attribute als JSON anzeigen |
| `show_counts` | `false` | `attributes.counts` anzeigen, falls eine Quelle es liefert; Air Traffic erzeugt dieses Attribut selbst nicht |
| `max_items` | `25` | Maximale Zahl angezeigter Flüge |
| `compact` | `false` | Hinweis für kompakte Kartenhöhe |

Das Bundle liegt unter dem technischen Pfad
`/air_traffic_merge/air-traffic-card.js`. Die Integration registriert es genau
einmal und schreibt weder Dashboards noch `.storage/lovelace.resources`.

## Migration

Die Umbenennung von **Air Traffic Merge** zu **Air Traffic** betrifft den
öffentlichen Namen und das Repository, nicht die technische Home-Assistant-
Domain:

- `air_traffic_merge` in Integrationspfad und Manifest behalten.
- Bestehende Config Entries, Entity IDs, Unique IDs und Optionen behalten.
- Bestehende HACS-Installation aktualisieren, nicht eine zweite Entity anlegen.
- `custom:air-traffic-merge-card` behalten, bis das neue Bundle geprüft wurde.
- Erst nach Prüfung eine Dashboard-Kopie auf `custom:air-traffic-card` umstellen.

Das frühere separate Kartenrepository wird nicht automatisch entfernt. Die
Lovelace-Ressource darf nicht allein deshalb gelöscht und das alte Repository
nicht allein deshalb archiviert werden, weil nun eine Karte integriert ist.
Diese Bereinigung braucht eine separat verifizierte Migration und eine bewusste
Entscheidung.

## Aktualisierung

1. Ein Home-Assistant-Backup erstellen.
2. Air Traffic in HACS auf die gewünschte veröffentlichte Version aktualisieren.
3. Home Assistant neu starten, wenn HACS dazu auffordert.
4. Bestehenden Config Entry und die drei Air-Traffic-Entities prüfen.
5. Ein bestehendes Dashboard öffnen und die aktuelle oder Legacy-Karte prüfen.

Die aktuelle Entwicklungsversion ist keine veröffentlichte Beta. Sie sollte
nicht allein deshalb produktiv installiert werden, weil die Versionsnummer im
Manifest sichtbar ist.

## Fehlerbehebung

- **Keine Flugzeuge:** Prüfen, ob die gewählte Entity ein Listenattribut
  `flights` oder `aircraft` liefert und nicht `unknown`/`unavailable` ist.
- **ADS-B-URL-Fehler:** Die normalisierte URL vom HA-Host öffnen und JSON mit
  einer `aircraft`-Liste prüfen.
- **Warnung wegen veralteter Daten:** `source_errors` und `data_stale` von
  `sensor.air_traffic_merged` prüfen; die letzten gültigen Quelldaten können
  weiterhin angezeigt werden.
- **Karte nicht gefunden:** Home-Assistant-Frontend neu laden und prüfen, ob
  die Integration geladen ist. Alte Kartenressource erst entfernen, wenn das
  neue Bundle in der Zielinstallation nachweislich funktioniert.
- **Fehlende Werte:** Die Quellformate unterscheiden sich; fehlende Werte
  werden absichtlich nicht erfunden.

## Datenschutz und Einschränkungen

Air Traffic liest die konfigurierten Home-Assistant-Entities und ruft im
URL-Modus den konfigurierten ADS-B-Endpunkt ab. Es gibt keinen FR24-Cloud-Login,
keinen Credential-Proxy, keinen Kartendienst und keine Anreicherung von
Flugstatusdaten. Bedingungen, Rate-Limits und Netzwerkschutz der jeweiligen
Quelle bleiben Verantwortung des Nutzers.

Die Karte ist eine responsive Liste mit Detailansicht, keine geografische Karte.
Der genaue Feldumfang hängt von der Quelle ab. Funktions-Screenshots sind nicht
eingebunden, weil kein verifizierter produktiver Screenshot vorliegt; die Bilder
im Repository sind ausschließlich Branding-Assets.

## Mitwirkung

Vor Issue oder Pull Request bitte [`CONTRIBUTING.md`](CONTRIBUTING.md) lesen.
Home-Assistant-Version, Air-Traffic-Version, Quellenmodus, minimales Karten-
YAML und anonymisierte Logs angeben. Niemals Tokens, API-Schlüssel, private URLs
oder genaue persönliche Standortdaten veröffentlichen.

## Lizenz

Air Traffic steht unter der [MIT-Lizenz](LICENSE).
