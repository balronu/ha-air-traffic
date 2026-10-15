import json
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
INTEGRATION = ROOT / "custom_components" / "air_traffic_merge"


class IntegrationContractTests(unittest.TestCase):
    def test_manifest_and_hacs_use_public_name_and_legacy_domain(self):
        manifest = json.loads((INTEGRATION / "manifest.json").read_text())
        hacs = json.loads((ROOT / "hacs.json").read_text())
        self.assertEqual(manifest["domain"], "air_traffic_merge")
        self.assertEqual(manifest["name"], "Air Traffic")
        self.assertEqual(hacs["name"], "Air Traffic")
        self.assertEqual(hacs["filename"], "air_traffic_merge")

    def test_frontend_contract_is_versioned_and_bundled(self):
        manifest = json.loads((INTEGRATION / "manifest.json").read_text())
        package = json.loads((ROOT / "frontend" / "package.json").read_text())
        lockfile = json.loads((ROOT / "frontend" / "package-lock.json").read_text())
        bundle = (INTEGRATION / "frontend" / "air-traffic-card.js").read_text()
        self.assertEqual(manifest["version"], package["version"])
        self.assertEqual(package["version"], lockfile["version"])
        self.assertIn('"air-traffic-card"', bundle)
        self.assertIn('"air-traffic-merge-card"', bundle)
        self.assertIn("customCards", bundle)

    def test_setup_contains_idempotent_frontend_registration(self):
        source = (INTEGRATION / "__init__.py").read_text()
        self.assertIn("frontend_registered", source)
        self.assertIn("async_register_static_paths", source)
        self.assertIn("add_extra_js_url", source)


if __name__ == "__main__":
    unittest.main()
