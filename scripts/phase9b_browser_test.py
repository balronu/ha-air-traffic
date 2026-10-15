"""Run an isolated Home Assistant instance and exercise its real Lovelace UI."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import Page, expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "phase9b-artifacts"
CONFIG = ARTIFACTS / "ha-config"
BASE_URL = "http://127.0.0.1:8123"


def write_test_config() -> None:
    (CONFIG / "custom_components").mkdir(parents=True, exist_ok=True)
    (CONFIG / "www").mkdir(exist_ok=True)
    shutil.copytree(
        ROOT / "custom_components" / "air_traffic_merge",
        CONFIG / "custom_components" / "air_traffic_merge",
        dirs_exist_ok=True,
    )
    (CONFIG / "configuration.yaml").write_text(
        """homeassistant:\n  name: Phase 9B Isolated HA\n\ndefault_config:\n\nhttp:\n  server_port: 8123\n\nlogger:\n  default: info\n  logs:\n    custom_components.air_traffic_merge: debug\n\nfrontend:\n\nlovelace:\n  mode: yaml\n\ntemplate:\n  - sensor:\n      - name: ADS-B Feed\n        unique_id: phase9b_adsb_feed\n        state: "2"\n        attributes:\n          aircraft:\n            - hex: abc123\n              flight: TEST123\n              lat: 50.0\n              lon: 8.0\n              alt_baro: 12000\n              gs: 410\n              track: 90\n            - hex: def456\n              flight: TEST456\n              lat: 50.2\n              lon: 8.2\n              alt_baro: 9000\n              gs: 320\n              track: 180\n          messages: 7\n          now: 1700000000\n      - name: FR24 Feed\n        unique_id: phase9b_fr24_feed\n        state: "1"\n        attributes:\n          flights:\n            - hex: fr24123\n              callsign: FR24123\n              registration: D-TEST\n              latitude: 51.0\n              longitude: 9.0\n              altitude: 11000\n              speed: 400\n      - name: Air Traffic Empty Fixture\n        unique_id: phase9b_empty\n        state: "0"\n        attributes:\n          flights: []\n          adsb_count: 0\n          fr24_count: 0\n          merged_count: 0\n      - name: Air Traffic Error Fixture\n        unique_id: phase9b_error\n        state: "0"\n        attributes:\n          flights: []\n          source_errors:\n            adsb: "Mock source error"\n      - name: Air Traffic Stale Fixture\n        unique_id: phase9b_stale\n        state: "1"\n        attributes:\n          flights:\n            - callsign: STALE1\n              hex: stale1\n          data_stale: true\n\ninput_number:\n  adsb_lat:\n    min: 0\n    max: 90\n    step: 0.1\n    initial: 50.0\n""",
        encoding="utf-8",
    )
    config_path = CONFIG / "configuration.yaml"
    config_path.write_text(
        config_path.read_text(encoding="utf-8").replace(
            "default_config:\n\n",
            "config:\napi:\nauth:\nonboarding:\nwebsocket_api:\n",
        ),
        encoding="utf-8",
    )
    config_path.write_text(
        config_path.read_text(encoding="utf-8").replace(
            "lat: 50.0", "lat: \"{{ states('input_number.adsb_lat') | float(50) }}\""
        ),
        encoding="utf-8",
    )
    (CONFIG / "ui-lovelace.yaml").write_text(
        """title: Phase 9B Air Traffic\nviews:\n  - title: Air Traffic\n    path: air-traffic\n    cards:\n      - type: custom:air-traffic-card\n        entity: sensor.air_traffic_merged\n        title: Modern Air Traffic\n        max_items: 25\n      - type: custom:air-traffic-merge-card\n        entity: sensor.air_traffic_merged\n        title: Legacy Air Traffic\n        max_items: 25\n      - type: custom:air-traffic-card\n        entity: sensor.air_traffic_empty_fixture\n        title: Empty Fixture\n      - type: custom:air-traffic-card\n        entity: sensor.air_traffic_error_fixture\n        title: Error Fixture\n      - type: custom:air-traffic-card\n        entity: sensor.air_traffic_stale_fixture\n        title: Stale Fixture\n""",
        encoding="utf-8",
    )


def wait_for_ha() -> None:
    import urllib.request

    deadline = time.time() + 180
    last_error = ""
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{BASE_URL}/", timeout=3) as response:
                if response.status in (200, 401):
                    return
        except Exception as exc:  # pragma: no cover - startup timing
            last_error = str(exc)
        time.sleep(2)
    raise RuntimeError(f"Home Assistant did not start: {last_error}")


def first_visible(page: Page, selectors: list[str]):
    for selector in selectors:
        locator = page.locator(selector).first
        if locator.is_visible():
            return locator
    raise AssertionError(f"No visible selector matched: {selectors}")


def onboard(page: Page) -> None:
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1000)
    if "/onboarding.html" not in page.url:
        return

    welcome = page.get_by_role("button", name=re.compile(r"Create my smart home|Erstelle dein Smart Home", re.I))
    if welcome.count() and welcome.first.is_visible():
        welcome.first.click(force=True)
        page.wait_for_timeout(700)

    for selector, value in (
        ("input[name='name']", "Phase 9B Tester"),
        ("input[name='username']", "phase9b"),
        ("input[name='password']", "Phase9B-Test-Only-Password-123!"),
        ("input[name='password_confirm']", "Phase9B-Test-Only-Password-123!"),
    ):
        locator = page.locator(selector)
        if locator.count():
            locator.fill(value)
    page.screenshot(path=str(ARTIFACTS / "onboarding-before-submit.png"), full_page=True)
    action_re = re.compile(r"Create account|Konto erstellen|Submit|Absenden", re.I)
    candidates = page.get_by_role("button", name=action_re)
    if not candidates.count():
        candidates = page.locator("ha-button, mwc-button").filter(has_text=action_re)
    visible = [candidates.nth(i) for i in range(candidates.count()) if candidates.nth(i).is_visible()]
    if not visible:
        (ARTIFACTS / "onboarding.html").write_text(page.content(), encoding="utf-8")
        raise AssertionError(f"Onboarding submit control not found; visible text: {page.locator('body').inner_text()[:2000]}")
    visible[-1].click(force=True)
    page.wait_for_timeout(700)
    for _ in range(4):
        buttons = page.locator("ha-button, mwc-button, button")
        visible = [buttons.nth(i) for i in range(buttons.count()) if buttons.nth(i).is_visible()]
        matching = [button for button in visible if re.search(r"Next|Weiter|Finish|Fertig|Submit|Absenden", button.inner_text(), re.I)]
        if not matching:
            break
        matching[0].click(force=True)
        page.wait_for_timeout(700)
    if "/onboarding.html" in page.url:
        page.screenshot(path=str(ARTIFACTS / "onboarding-after-submit.png"), full_page=True)
        (ARTIFACTS / "onboarding-after-submit.html").write_text(page.content(), encoding="utf-8")
        raise AssertionError(
            f"Onboarding did not complete: {page.url}; visible text: {page.locator('body').inner_text()[:3000]}"
        )


def ws(page: Page, message: dict) -> dict:
    result = page.evaluate(
        """async (message) => {
          const hass = document.querySelector('home-assistant')?.hass;
          if (!hass) throw new Error('Home Assistant frontend object unavailable');
          return await hass.callWS(message);
        }""",
        message,
    )
    if not isinstance(result, dict):
        raise AssertionError(f"Unexpected WebSocket result: {result!r}")
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
        raise RuntimeError("hass executable is unavailable on the isolated runner")
    with log_path.open("w", encoding="utf-8") as log_file:
        process = subprocess.Popen([hass, "-c", str(CONFIG)], stdout=log_file, stderr=subprocess.STDOUT, cwd=ROOT)
    console: list[str] = []
    errors: list[str] = []
    try:
        wait_for_ha()
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1440, "height": 1000})
            page.on("console", lambda message: console.append(f"{message.type}: {message.text}"))
            page.on("pageerror", lambda error: errors.append(str(error)))
            onboard(page)
            page.goto(BASE_URL + "/lovelace/0", wait_until="networkidle")
            entry_id = configure_integration(page)
            configure_options(page, entry_id)
            ws(page, {"type": "config_entries/unload", "entry_id": entry_id})
            ws(page, {"type": "config_entries/reload", "entry_id": entry_id})
            page.goto(BASE_URL + "/lovelace/0", wait_until="networkidle")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(ARTIFACTS / "desktop.png"), full_page=True)
            assert page.locator("air-traffic-card").count() >= 4
            assert page.get_by_text("TEST123", exact=True).count() >= 1
            assert page.get_by_text("TEST456", exact=True).count() >= 1
            assert page.get_by_text("Keine Flugzeuge vorhanden.", exact=True).count() >= 1
            assert page.get_by_text("Mock source error", exact=False).count() >= 1
            assert page.get_by_text("Veraltete Quelldaten", exact=False).count() >= 1
            assert page.locator("script[src*='/air_traffic_merge/air-traffic-card.js']").count() == 1
            custom_cards = page.evaluate("() => window.customCards?.filter((card) => card.type.includes('air-traffic'))")
            assert len(custom_cards or []) == 2, custom_cards
            page.locator("air-traffic-card").first.locator("article.flight").first.click()
            expect(page.locator("air-traffic-card").first.locator(".detail")).to_be_visible()
            page.evaluate("""async () => { const h = document.querySelector('home-assistant').hass; await h.callService('input_number', 'set_value', {entity_id:'input_number.adsb_lat', value:51.0}); }""")
            page.wait_for_timeout(1500)
            page.set_viewport_size({"width": 390, "height": 844})
            page.screenshot(path=str(ARTIFACTS / "mobile.png"), full_page=True)
            page.screenshot(path=str(ARTIFACTS / "legacy-card.png"), full_page=True)
            page.emulate_media(color_scheme="dark")
            page.screenshot(path=str(ARTIFACTS / "dark-theme.png"), full_page=True)
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
    integration_errors = [
        line for line in ha_log.splitlines()
        if "ERROR" in line and "custom_components.air_traffic_merge" in line
    ]
    if integration_errors:
        raise AssertionError("Integration errors in Home Assistant log:\n" + "\n".join(integration_errors))
    (ARTIFACTS / "browser-console.txt").write_text("\n".join(console), encoding="utf-8")
    (ARTIFACTS / "browser-errors.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")
    print("Phase 9B isolated Home Assistant + browser validation passed")


if __name__ == "__main__":
    main()
