"""Run isolated HA 2026.10.1 onboarding and real Lovelace browser checks."""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

from playwright.sync_api import Page, expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "phase9c-artifacts"
CONFIG = ARTIFACTS / "ha-config"
BASE_URL = "http://127.0.0.1:8123"


def write_test_config() -> None:
    (CONFIG / "custom_components").mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "custom_components" / "air_traffic_merge", CONFIG / "custom_components" / "air_traffic_merge", dirs_exist_ok=True)
    (CONFIG / "www").mkdir(exist_ok=True)
    (CONFIG / "configuration.yaml").write_text(
        """homeassistant:
  name: Phase 9C Isolated HA
config:
api:
auth:
onboarding:
websocket_api:
http:
  server_port: 8123
logger:
  default: info
  logs:
    custom_components.air_traffic_merge: debug
frontend:
lovelace:
  mode: yaml
template:
  - sensor:
      - name: ADS-B Feed
        unique_id: phase9c_adsb_feed
        state: "2"
        attributes:
          aircraft: "{{ [{'hex': 'abc123', 'flight': 'TEST123', 'lat': states('input_number.adsb_lat') | float(50), 'lon': 8.0, 'alt_baro': 12000, 'gs': 410, 'track': 90}, {'hex': 'def456', 'flight': 'TEST456', 'lat': 50.2, 'lon': 8.2, 'alt_baro': 9000, 'gs': 320, 'track': 180}] }}"
          messages: 7
          now: 1700000000
      - name: FR24 Feed
        unique_id: phase9c_fr24_feed
        state: "1"
        attributes:
          flights: "{{ [{'hex': 'fr24123', 'callsign': 'FR24123', 'registration': 'D-TEST', 'latitude': 51.0, 'longitude': 9.0, 'altitude': 11000, 'speed': 400}] }}"
      - name: Air Traffic Empty Fixture
        unique_id: phase9c_empty
        state: "0"
        attributes: {flights: "{{ [] }}", adsb_count: 0, fr24_count: 0, merged_count: 0}
      - name: Air Traffic Error Fixture
        unique_id: phase9c_error
        state: "0"
        attributes: {flights: "{{ [] }}", source_errors: "{{ {'adsb': 'Mock source error'} }}"}
      - name: Air Traffic Stale Fixture
        unique_id: phase9c_stale
        state: "1"
        attributes: {flights: "{{ [{'callsign': 'STALE1', 'hex': 'stale1'}] }}", data_stale: true}
input_number:
  adsb_lat:
    min: 0
    max: 90
    step: 0.1
    initial: 50.0
""",
        encoding="utf-8",
    )
    (CONFIG / "ui-lovelace.yaml").write_text(
        """title: Phase 9C Air Traffic
views:
  - title: Air Traffic
    path: air-traffic
    cards:
      - type: custom:air-traffic-card
        entity: sensor.air_traffic_merged
        title: Modern Air Traffic
        max_items: 25
      - type: custom:air-traffic-merge-card
        entity: sensor.air_traffic_merged
        title: Legacy Air Traffic
        max_items: 25
      - type: custom:air-traffic-card
        entity: sensor.air_traffic_empty_fixture
        title: Empty Fixture
      - type: custom:air-traffic-card
        entity: sensor.air_traffic_error_fixture
        title: Error Fixture
      - type: custom:air-traffic-card
        entity: sensor.air_traffic_stale_fixture
        title: Stale Fixture
""",
        encoding="utf-8",
    )


def wait_for_ha() -> None:
    import urllib.request

    deadline = time.time() + 180
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{BASE_URL}/", timeout=3) as response:
                if response.status in (200, 401):
                    return
        except Exception:
            pass
        time.sleep(2)
    raise RuntimeError("Home Assistant did not start")


def onboard(page: Page) -> None:
    """Use HA's browser-facing onboarding APIs; do not edit .storage files."""
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1000)
    if "/onboarding.html" not in page.url:
        return
    page.screenshot(path=str(ARTIFACTS / "onboarding-before-api.png"), full_page=True)
    result = page.evaluate(
        """async () => {
          const base = location.origin;
          const clientId = `${base}/`;
          const user = await fetch(`${base}/api/onboarding/users`, {method: 'POST',
            headers: {'Content-Type': 'application/json'}, body: JSON.stringify({
              name: 'Phase 9C CI Tester', username: 'phase9c-ci',
              password: 'Phase9C-Test-Only-Password-123!', client_id: clientId, language: 'en'})});
          if (!user.ok) throw new Error(`onboarding user failed: ${user.status} ${await user.text()}`);
          const {auth_code} = await user.json();
          const form = new FormData(); form.append('client_id', clientId);
          form.append('code', auth_code); form.append('grant_type', 'authorization_code');
          const tokenResponse = await fetch(`${base}/auth/token`, {method: 'POST', body: form});
          if (!tokenResponse.ok) throw new Error(`auth token failed: ${tokenResponse.status} ${await tokenResponse.text()}`);
          const tokens = await tokenResponse.json(); tokens.hassUrl = base;
          tokens.clientId = clientId; tokens.expires = Date.now() + tokens.expires_in * 1000;
          const callWs = (message) => new Promise((resolve, reject) => {
            const socket = new WebSocket(`ws://${location.host}/api/websocket`);
            socket.onmessage = (event) => {
              const value = JSON.parse(event.data);
              if (value.type === 'auth_required') socket.send(JSON.stringify({type: 'auth', access_token: tokens.access_token}));
              else if (value.type === 'auth_ok') socket.send(JSON.stringify({...message, id: 1}));
              else if (value.id === 1) { socket.close(); value.success ? resolve(value.result) : reject(new Error(JSON.stringify(value))); }
            };
            socket.onerror = () => reject(new Error('HA WebSocket error'));
          });
          await callWs({type: 'config/core/update', location_name: 'Phase 9C CI', latitude: 50.1109,
            longitude: 8.6821, elevation: 100, unit_system: 'metric', time_zone: 'Europe/Berlin',
            currency: 'EUR', country: 'DE', language: 'en'});
          const api = async (path, body) => {
            const response = await fetch(`${base}/api/${path}`, {method: 'POST',
              headers: {'Authorization': `Bearer ${tokens.access_token}`, 'Content-Type': 'application/json'},
              body: body ? JSON.stringify(body) : undefined});
            if (!response.ok) throw new Error(`${path} failed: ${response.status} ${await response.text()}`);
            return response.json();
          };
          await api('onboarding/core_config'); await api('onboarding/analytics');
          await api('onboarding/integration', {client_id: clientId, redirect_uri: `${base}/?auth_callback=1`});
          localStorage.setItem('hassTokens', JSON.stringify(tokens));
          return {steps: await (await fetch(`${base}/api/onboarding`)).json()};
        }"""
    )
    assert result["steps"][0]["done"] is True, result
    page.goto(BASE_URL + "/lovelace/0", wait_until="networkidle")
    page.wait_for_function("() => Boolean(document.querySelector('home-assistant')?.hass)", timeout=60000)
    if "/onboarding.html" in page.url:
        page.screenshot(path=str(ARTIFACTS / "onboarding-api-failure.png"), full_page=True)
        raise AssertionError(f"API onboarding did not complete: {page.url}")


def ws(page: Page, message: dict) -> dict:
    result = page.evaluate("""async (message) => await document.querySelector('home-assistant').hass.callWS(message)""", message)
    assert isinstance(result, dict), result
    return result


def configure_integration(page: Page) -> str:
    flow = ws(page, {"type": "config_entries/flow", "handler": "air_traffic_merge", "show_advanced": False})
    flow_id = flow["flow_id"]
    flow = ws(page, {"type": "config_entries/flow", "flow_id": flow_id, "user_input": {"source_mode": "both", "enable_tracking": False}})
    assert flow["step_id"] == "fr24"
    flow = ws(page, {"type": "config_entries/flow", "flow_id": flow_id, "user_input": {"fr24_entity": "sensor.fr24_feed"}})
    assert flow["step_id"] == "adsb_source"
    flow = ws(page, {"type": "config_entries/flow", "flow_id": flow_id, "user_input": {"adsb_source": "entity", "scan_interval": 10}})
    assert flow["step_id"] == "adsb_entity"
    flow = ws(page, {"type": "config_entries/flow", "flow_id": flow_id, "user_input": {"adsb_entity": "sensor.adsb_feed"}})
    assert flow["type"] == "create_entry", flow
    return flow["result"]["entry_id"]


def configure_options(page: Page, entry_id: str) -> None:
    flow = ws(page, {"type": "config_entries/options", "entry_id": entry_id})
    flow_id = flow["flow_id"]
    flow = ws(page, {"type": "config_entries/options", "flow_id": flow_id, "user_input": {"scan_interval": 20, "enable_tracking": True}})
    assert flow["step_id"] == "tracking"
    flow = ws(page, {"type": "config_entries/options", "flow_id": flow_id, "user_input": {"track_mode": "callsign", "track_callsigns": "TEST123"}})
    assert flow["type"] == "create_entry", flow


def main() -> None:
    ARTIFACTS.mkdir(exist_ok=True)
    write_test_config()
    log_path = ARTIFACTS / "home-assistant.log"
    hass = shutil.which("hass")
    if not hass:
        raise RuntimeError("hass executable is unavailable")
    console: list[str] = []
    errors: list[str] = []
    with log_path.open("w", encoding="utf-8") as log_file:
        process = subprocess.Popen([hass, "-c", str(CONFIG)], stdout=log_file, stderr=subprocess.STDOUT, cwd=ROOT)
    try:
        wait_for_ha()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1000})
            page.on("console", lambda message: console.append(f"{message.type}: {message.text}"))
            page.on("pageerror", lambda error: errors.append(str(error)))
            onboard(page)
            entry_id = configure_integration(page)
            configure_options(page, entry_id)
            ws(page, {"type": "config_entries/unload", "entry_id": entry_id})
            ws(page, {"type": "config_entries/reload", "entry_id": entry_id})
            page.goto(BASE_URL + "/lovelace/0", wait_until="networkidle")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(ARTIFACTS / "desktop-light.png"), full_page=True)
            assert page.locator("air-traffic-card").count() >= 4
            assert page.get_by_text("TEST123", exact=True).count() >= 1
            assert page.get_by_text("TEST456", exact=True).count() >= 1
            assert page.get_by_text("No aircraft available.", exact=True).count() >= 1
            assert page.get_by_text("Mock source error", exact=False).count() >= 1
            assert page.get_by_text("Stale source data", exact=False).count() >= 1
            assert page.locator("script[src*='/air_traffic_merge/air-traffic-card.js']").count() == 1
            custom_cards = page.evaluate("() => window.customCards?.filter((card) => card.type.includes('air-traffic'))")
            assert len(custom_cards or []) == 2, custom_cards
            page.locator("air-traffic-card").first.locator("article.flight").first.click()
            expect(page.locator("air-traffic-card").first.locator(".detail")).to_be_visible()
            page.evaluate("""async () => await document.querySelector('home-assistant').hass.callService('input_number', 'set_value', {entity_id:'input_number.adsb_lat', value:51.0})""")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(ARTIFACTS / "legacy-card.png"), full_page=True)
            page.set_viewport_size({"width": 390, "height": 844})
            page.screenshot(path=str(ARTIFACTS / "mobile-light.png"), full_page=True)
            page.emulate_media(color_scheme="dark")
            page.screenshot(path=str(ARTIFACTS / "mobile-dark.png"), full_page=True)
            page.set_viewport_size({"width": 1440, "height": 1000})
            page.screenshot(path=str(ARTIFACTS / "desktop-dark.png"), full_page=True)
            assert not errors, errors
            browser.close()
    finally:
        process.terminate()
        try:
            process.wait(timeout=20)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=10)
    ha_log = log_path.read_text(encoding="utf-8", errors="replace")
    integration_errors = [line for line in ha_log.splitlines() if "ERROR" in line and "custom_components.air_traffic_merge" in line]
    if integration_errors:
        raise AssertionError("Integration errors in Home Assistant log:\n" + "\n".join(integration_errors))
    (ARTIFACTS / "browser-console.txt").write_text("\n".join(console), encoding="utf-8")
    (ARTIFACTS / "browser-errors.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")
    print("Phase 9C isolated Home Assistant + browser validation passed")


if __name__ == "__main__":
    main()
