# Changelog

## v1.4.0-beta.1 (draft)

- public branding prepared as **Air Traffic**
- integrated Lovelace card assets and legacy card compatibility documented
- generated logo, social preview and README banner added under `images/branding/`
- README, German README, contributing guide and GitHub templates prepared
- release notes drafted; no tag or release published

## v1.3.1
- aus dem aktuell funktionierenden Home-Assistant-Stand unter `/config/custom_components/air_traffic_merge` neu aufgebaut
- Runtime-Fehler durch `hass.helpers.entity_component.async_update_entity` entfernt
- Tracking-Count-Sensor wird direkt aus dem gemeinsamen Store aktualisiert
- echte GitHub-/HACS-Metadaten für `balronu/air-traffic-merge`
- Validierungs-Workflow für Python- und JSON-Dateien ergänzt

## v1.3.0
- HACS-/GitHub-Repo bereinigt
- keine `__pycache__`-Dateien mehr im Repo
- README für direkte GitHub-/HACS-Nutzung ergänzt
- `adsb.im`-Feldmapping für `aircraft.json`
- kein Zugriff über `hass.helpers`
