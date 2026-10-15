import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
INTEGRATION = ROOT / "custom_components" / "air_traffic_merge"


class MigrationContractTests(unittest.TestCase):
    def test_legacy_entity_and_event_contracts_are_preserved(self):
        sensor = (INTEGRATION / "sensor.py").read_text()
        binary_sensor = (INTEGRATION / "binary_sensor.py").read_text()
        coordinator = (INTEGRATION / "coordinator.py").read_text()
        self.assertIn('entry.entry_id}_merged"', sensor)
        self.assertIn('entry.entry_id}_tracked_count"', sensor)
        self.assertIn('entry.entry_id}_tracked_present"', binary_sensor)
        self.assertIn('f"{DOMAIN}_tracked"', coordinator)

    def test_legacy_sensor_attributes_are_present(self):
        sensor = (INTEGRATION / "sensor.py").read_text()
        for attribute in ("aircraft", "messages", "now", "last_update", "flights"):
            self.assertIn(f'"{attribute}"', sensor)

    def test_legacy_card_contract_is_registered_and_documented(self):
        bundle = (INTEGRATION / "frontend" / "air-traffic-card.js").read_text()
        readme = (ROOT / "README.md").read_text()
        self.assertIn('"air-traffic-merge-card"', bundle)
        self.assertIn("custom:air-traffic-merge-card", readme)
        self.assertIn("custom:air-traffic-card", readme)

    def test_config_entry_data_keys_remain_unchanged(self):
        const = (INTEGRATION / "const.py").read_text()
        for key in ("source_mode", "fr24_entity", "adsb_source", "adsb_url", "adsb_entity", "scan_interval", "enable_tracking", "track_mode", "track_callsigns", "track_registrations"):
            self.assertIn(f'"{key}"', const)


if __name__ == "__main__":
    unittest.main()
