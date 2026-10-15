"""Run the complete Phase 9D browser matrix in an isolated HA instance."""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path

from playwright.sync_api import Page, expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "phase9d-artifacts"
CONFIG = ARTIFACTS / "ha-config"
BASE_URL = "http://127.0.0.1:8123"


def write_test_config() -> None:
    (CONFIG / "custom_components").mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "custom_components" / "air_traffic_merge", CONFIG / "custom_components" / "air_traffic_merge", dirs_exist_ok=True)
    (CONFIG / "configuration.yaml").write_text(
        """homeassistant:
  name: Phase 9D Isolated HA
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
        unique_id: phase9d_adsb_feed
        state: "2"
        attributes:
          aircraft: "{{ [{'hex': 'abc123', 'flight': 'TEST123', 'lat': states('input_number.adsb_lat') | float(50), 'lon': 8.0, 'alt_baro': 12000, 'gs': 410, 'track': 90}, {'hex': 'def456', 'flight': 'TEST456', 'lat': 50.2, 'lon': 8.2, 'alt_baro': 9000, 'gs': 320, 'track': 180}] }}"
          messages: 7
          now: 1700000000
      - name: FR24 Feed
        unique_id: phase9d_fr24_feed
        state: "1"
        attributes:
          flights: "{{ [{'hex': 'fr24123', 'callsign': 'FR24123', 'registration': 'D-TEST', 'latitude': 51.0, 'longitude': 9.0, 'altitude': 11000, 'speed': 400}] }}"
      - name: Air Traffic Empty Fixture
        unique_id: phase9d_empty
        state: "0"
        attributes: {flights: "{{ [] }}", adsb_count: 0, fr24_count: 0, merged_count: 0}
      - name: Air Traffic Error Fixture
        unique_id: phase9d_error
        state: "0"
        attributes: {flights: "{{ [] }}", source_errors: "{{ {'adsb': 'Mock source error'} }}"}
      - name: Air Traffic Stale Fixture
        unique_id: phase9d_stale
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
        """title: Phase 9D Air Traffic
views:
  - title: Empty
    path: empty
    cards: []
  - title: Native
    path: native
    cards:
      - type: markdown
        content: "Native Home Assistant card"
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
            time.sleep(2)
    raise RuntimeError("Home Assistant did not start")


def onboard(page: Page) -> None:
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1000)
    if "/onboarding.html" not in page.url:
        return
    page.screenshot(path=str(ARTIFACTS / "onboarding-before-api.png"), full_page=True)
    result = page.evaluate(
        """async () => {
          const base = location.origin; const clientId = `${base}/`;
          const user = await fetch(`${base}/api/onboarding/users`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({name: 'Phase 9D CI Tester', username: 'phase9d-ci', password: 'Phase9D-Test-Only-Password-123!', client_id: clientId, language: 'en'})});
          if (!user.ok) throw new Error(`onboarding user failed: ${user.status} ${await user.text()}`);
          const {auth_code} = await user.json(); const form = new FormData(); form.append('client_id', clientId); form.append('code', auth_code); form.append('grant_type', 'authorization_code');
          const tokenResponse = await fetch(`${base}/auth/token`, {method: 'POST', body: form}); if (!tokenResponse.ok) throw new Error(`auth token failed: ${tokenResponse.status} ${await tokenResponse.text()}`);
          const tokens = await tokenResponse.json(); tokens.hassUrl = base; tokens.clientId = clientId; tokens.expires = Date.now() + tokens.expires_in * 1000;
          const callWs = (message) => new Promise((resolve, reject) => { const socket = new WebSocket(`ws://${location.host}/api/websocket`); socket.onmessage = (event) => { const value = JSON.parse(event.data); if (value.type === 'auth_required') socket.send(JSON.stringify({type: 'auth', access_token: tokens.access_token})); else if (value.type === 'auth_ok') socket.send(JSON.stringify({...message, id: 1})); else if (value.id === 1) { socket.close(); value.success ? resolve(value.result) : reject(new Error(JSON.stringify(value))); } }; socket.onerror = () => reject(new Error('HA WebSocket error')); });
          await callWs({type: 'config/core/update', location_name: 'Phase 9D CI', latitude: 50.1109, longitude: 8.6821, elevation: 100, unit_system: 'metric', time_zone: 'Europe/Berlin', currency: 'EUR', country: 'DE', language: 'en'});
          const api = async (path, body) => { const response = await fetch(`${base}/api/${path}`, {method: 'POST', headers: {'Authorization': `Bearer ${tokens.access_token}`, 'Content-Type': 'application/json'}, body: body ? JSON.stringify(body) : undefined}); if (!response.ok) throw new Error(`${path} failed: ${response.status} ${await response.text()}`); return response.json(); };
          await api('onboarding/core_config'); await api('onboarding/analytics'); await api('onboarding/integration', {client_id: clientId, redirect_uri: `${base}/?auth_callback=1`}); localStorage.setItem('hassTokens', JSON.stringify(tokens));
          return {steps: await (await fetch(`${base}/api/onboarding`)).json()};
        }"""
    )
    assert result["steps"][0]["done"] is True, result
    page.goto(BASE_URL + "/lovelace/empty", wait_until="networkidle")
    page.wait_for_function("() => Boolean(document.querySelector('home-assistant')?.hass)", timeout=60000)
    if "/onboarding.html" in page.url:
        raise AssertionError(f"API onboarding did not complete: {page.url}")


def api(page: Page, method: str, path: str, data: dict | None = None) -> dict:
    result = page.evaluate("""async ({method, path, data}) => document.querySelector('home-assistant').hass.callApi(method, path, data, {'HA-Frontend-Base': location.origin})""", {"method": method, "path": path, "data": data})
    assert isinstance(result, dict), result
    return result


def configure_integration(page: Page) -> str:
    flow = api(page, "POST", "config/config_entries/flow", {"handler": "air_traffic_merge"}); flow_id = flow["flow_id"]
    flow = api(page, "POST", f"config/config_entries/flow/{flow_id}", {"source_mode": "both", "enable_tracking": False}); assert flow["step_id"] == "fr24"
    flow = api(page, "POST", f"config/config_entries/flow/{flow_id}", {"fr24_entity": "sensor.fr24_feed"}); assert flow["step_id"] == "adsb_source"
    flow = api(page, "POST", f"config/config_entries/flow/{flow_id}", {"adsb_source": "entity", "scan_interval": 5}); assert flow["step_id"] == "adsb_entity"
    # HA slugifies “ADS-B Feed” to sensor.ads_b_feed.
    flow = api(page, "POST", f"config/config_entries/flow/{flow_id}", {"adsb_entity": "sensor.ads_b_feed"}); assert flow["type"] == "create_entry", flow
    return flow["result"]["entry_id"]


def configure_options(page: Page, entry_id: str) -> None:
    flow = api(page, "POST", "config/config_entries/options/flow", {"handler": entry_id}); flow_id = flow["flow_id"]
    flow = api(page, "POST", f"config/config_entries/options/flow/{flow_id}", {"scan_interval": 5, "enable_tracking": True}); assert flow["step_id"] == "tracking"
    flow = api(page, "POST", f"config/config_entries/options/flow/{flow_id}", {"track_mode": "callsign", "track_callsigns": "TEST123"}); assert flow["type"] == "create_entry", flow


def save_diagnostics(console: list[str], errors: list[str], requests: list[str], websockets: list[str]) -> None:
    (ARTIFACTS / "browser-console.txt").write_text("\n".join(console), encoding="utf-8")
    (ARTIFACTS / "browser-errors.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")
    (ARTIFACTS / "browser-request-failures.txt").write_text("\n".join(requests), encoding="utf-8")
    (ARTIFACTS / "browser-websockets.txt").write_text("\n".join(websockets), encoding="utf-8")


def main() -> None:
    ARTIFACTS.mkdir(exist_ok=True); write_test_config(); log_path = ARTIFACTS / "home-assistant.log"
    hass = shutil.which("hass");
    if not hass: raise RuntimeError("hass executable is unavailable")
    console: list[str] = []; errors: list[str] = []; requests: list[str] = []; websockets: list[str] = []; process = None
    try:
        with log_path.open("w", encoding="utf-8") as log_file: process = subprocess.Popen([hass, "-c", str(CONFIG)], stdout=log_file, stderr=subprocess.STDOUT, cwd=ROOT)
        wait_for_ha()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(); page = browser.new_page(viewport={"width": 1440, "height": 1000})
            page.add_init_script("""() => { window.__phase9dErrors = []; addEventListener('error', e => window.__phase9dErrors.push({type:'error', message:e.message, stack:e.error?.stack || '', source:e.filename})); addEventListener('unhandledrejection', e => window.__phase9dErrors.push({type:'unhandledrejection', message:String(e.reason), stack:e.reason?.stack || ''})); }""")
            page.on("console", lambda message: console.append(f"{message.type}: {message.text}")); page.on("pageerror", lambda error: errors.append(f"{getattr(error, 'name', 'Error')}: {getattr(error, 'message', str(error))}\n{getattr(error, 'stack', '')}")); page.on("requestfailed", lambda request: requests.append(f"{request.method} {request.url}: {request.failure}")); page.on("response", lambda response: requests.append(f"HTTP {response.status} {response.request.method} {response.url}") if response.status >= 400 else None)
            page.on("websocket", lambda socket: (websockets.append(f"OPEN {socket.url}"), socket.on("framereceived", lambda payload: websockets.append(f"RECV {socket.url} {str(payload)[:500]}")), socket.on("framesent", lambda payload: websockets.append(f"SEND {socket.url} {str(payload)[:500]}")), socket.on("close", lambda: websockets.append(f"CLOSE {socket.url}"))))
            onboard(page)
            page.goto(BASE_URL + "/lovelace/empty", wait_until="networkidle"); page.wait_for_selector("hui-view", timeout=60000); page.screenshot(path=str(ARTIFACTS / "01-empty-lovelace.png"), full_page=True); assert page.locator("air-traffic-card").count() == 0
            page.goto(BASE_URL + "/lovelace/native", wait_until="networkidle"); page.wait_for_selector("hui-view", timeout=60000); expect(page.get_by_text("Native Home Assistant card", exact=True)).to_be_visible(); page.screenshot(path=str(ARTIFACTS / "02-native-card.png"), full_page=True); assert page.locator("air-traffic-card").count() == 0
            entry_id = configure_integration(page); configure_options(page, entry_id); api(page, "POST", f"config/config_entries/entry/{entry_id}/reload")
            page.goto(BASE_URL + "/lovelace/air-traffic", wait_until="networkidle"); page.wait_for_selector("hui-view", timeout=60000); page.wait_for_timeout(2000); page.screenshot(path=str(ARTIFACTS / "03-desktop-light.png"), full_page=True)
            assert page.locator("air-traffic-card").count() == 5; assert page.get_by_text("TEST123", exact=True).count() >= 1; assert page.get_by_text("TEST456", exact=True).count() >= 1; assert page.get_by_text("Keine Flugzeuge vorhanden.", exact=True).count() >= 1; assert page.get_by_text("Mock source error", exact=False).count() >= 1; assert page.get_by_text("Veraltete Quelldaten", exact=False).count() >= 1
            assert page.locator("script[src*='/air_traffic_merge/air-traffic-card.js']").count() == 1; custom_cards = page.evaluate("() => window.customCards?.filter((card) => card.type.includes('air-traffic'))"); assert len(custom_cards or []) == 2, custom_cards
            modern = page.locator("air-traffic-card").first; modern.locator("article.flight").first.click(); expect(modern.locator(".detail")).to_be_visible(); assert "Position:" in modern.locator(".detail").inner_text()
            page.evaluate("""async () => await document.querySelector('home-assistant').hass.callService('input_number', 'set_value', {entity_id:'input_number.adsb_lat', value:51.0})"""); page.wait_for_function("() => document.querySelector('home-assistant')?.hass?.states?.['sensor.air_traffic_merged']?.attributes?.flights?.some(f => f.callsign === 'TEST123' && Number(f.latitude) === 51)", timeout=15000); assert "51" in modern.locator(".detail").inner_text(); page.screenshot(path=str(ARTIFACTS / "04-aircraft-update-detail.png"), full_page=True)
            page.set_viewport_size({"width": 390, "height": 844}); page.screenshot(path=str(ARTIFACTS / "05-mobile-light.png"), full_page=True); page.emulate_media(color_scheme="dark"); page.screenshot(path=str(ARTIFACTS / "06-mobile-dark.png"), full_page=True); page.set_viewport_size({"width": 1440, "height": 1000}); page.screenshot(path=str(ARTIFACTS / "07-desktop-dark.png"), full_page=True); assert not errors, errors; browser.close()
    finally:
        save_diagnostics(console, errors, requests, websockets)
        if process is not None:
            process.terminate()
            try: process.wait(timeout=20)
            except subprocess.TimeoutExpired: process.kill(); process.wait(timeout=10)
        if log_path.exists():
            log = log_path.read_text(encoding="utf-8", errors="replace"); integration_errors = [line for line in log.splitlines() if "ERROR" in line and "custom_components.air_traffic_merge" in line]; (ARTIFACTS / "integration-errors.txt").write_text("\n".join(integration_errors), encoding="utf-8")
            if integration_errors: raise AssertionError("Integration errors in Home Assistant log:\n" + "\n".join(integration_errors))
    print("Phase 9D isolated Home Assistant + browser validation passed")


if __name__ == "__main__": main()
