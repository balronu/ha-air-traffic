# Air Traffic

Home-Assistant-Integration zur Zusammenführung eines vorhandenen
Flightradar24-Sensors mit lokalen ADS-B-Daten. Die Lovelace-Karte ist direkt in
die Integration eingebaut.

## Technische Kompatibilität

Die interne Domain `air_traffic_merge`, bestehende Entity IDs, Unique IDs,
Config Entries, Optionen und das Ereignis `air_traffic_merge_tracked` bleiben
erhalten. Die öffentliche Bezeichnung lautet ausschließlich **Air Traffic**.

Unterstützte Quellmodi sind FR24, ADS-B per URL, ADS-B per Entity und die
Kombination beider Quellen. Fehlende Datenfelder werden nicht erfunden.

## Karte

```yaml
type: custom:air-traffic-card
entity: sensor.air_traffic_merged
title: Air Traffic
show_status: true
max_items: 25
```

Bestehende Dashboards mit `custom:air-traffic-merge-card` bleiben über einen
Legacy-Alias kompatibel. Die Integration registriert das versionierte Bundle
`/air_traffic_merge/air-traffic-card.js?v=1.4.0-beta.1` automatisch und schreibt
keine Lovelace-Resource-Dateien.

## Entwicklungsstatus

Dies ist ein lokaler Phase-2-Kandidat auf dem Branch
`work/air-traffic-modernization`. Das Zielrepository wurde noch nicht erstellt,
und es wurden keine produktiven Home-Assistant-Daten verändert.
