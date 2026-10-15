"""Validate the production card bundle with only the required HA surface mocked."""

from __future__ import annotations

import json
import shutil
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "phase9d-artifacts" / "component"


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "custom_components/air_traffic_merge/frontend/air-traffic-card.js", ARTIFACTS / "air-traffic-card.js")
    (ARTIFACTS / "index.html").write_text(
        """<!doctype html><meta charset='utf-8'><title>Air Traffic component harness</title>
<home-assistant></home-assistant><main id='cards'></main>
<script>customElements.define('home-assistant', class extends HTMLElement {});</script>
<script type='module' src='/air-traffic-card.js'></script>
<script>
window.addEventListener('load', () => {
  const states = {
    'sensor.flights': {state:'2', attributes:{flights:[{callsign:'TEST123',hex:'abc123',source:'ADSB',latitude:50,longitude:8},{callsign:'TEST456',hex:'def456',source:'ADSB',latitude:50.2,longitude:8.2}], data_stale:false}},
    'sensor.empty': {state:'0', attributes:{flights:[]}},
    'sensor.error': {state:'0', attributes:{flights:[], source_errors:{adsb:'Mock source error'}}},
    'sensor.stale': {state:'1', attributes:{flights:[{callsign:'STALE1',hex:'stale1'}], data_stale:true}}
  };
  const hass = {states}; document.querySelector('home-assistant').hass = hass;
  for (const [tag, entity, title] of [['air-traffic-card','sensor.flights','Modern'],['air-traffic-merge-card','sensor.flights','Legacy'],['air-traffic-card','sensor.empty','Empty'],['air-traffic-card','sensor.error','Error'],['air-traffic-card','sensor.stale','Stale']]) { const card=document.createElement(tag); card.setConfig({type:`custom:${tag}`,entity,title,max_items:25}); card.hass=hass; document.querySelector('#cards').append(card); }
});
</script>""",
        encoding="utf-8",
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=str(ARTIFACTS), **kwargs))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    errors: list[str] = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(); page = browser.new_page(viewport={"width": 1200, "height": 800}); page.on("pageerror", lambda error: errors.append(repr(error)))
            page.goto(f"http://127.0.0.1:{server.server_port}/index.html", wait_until="networkidle"); page.wait_for_timeout(500)
            page.locator("air-traffic-card").nth(0).locator("article.flight").first.click()
            checks = {"modern": page.locator("air-traffic-card").count() == 4, "legacy": page.locator("air-traffic-merge-card").count() == 1, "custom_cards": page.evaluate("() => window.customCards.filter((entry) => entry.type.includes('air-traffic')).length") == 2, "flights": page.get_by_text("TEST123", exact=True).count() >= 1, "legacy_flight": page.locator("air-traffic-merge-card").get_by_text("TEST456", exact=True).count() >= 1, "detail": page.locator("air-traffic-card").nth(0).locator(".detail").count() == 1, "empty": page.get_by_text("Keine Flugzeuge vorhanden.", exact=True).count() >= 1, "error": page.get_by_text("Mock source error", exact=False).count() >= 1, "stale": page.get_by_text("Veraltete Quelldaten", exact=False).count() >= 1}
            (ARTIFACTS / "checks.json").write_text(json.dumps(checks, indent=2), encoding="utf-8"); page.screenshot(path=str(ARTIFACTS / "component-desktop.png"), full_page=True); browser.close()
    finally:
        server.shutdown(); (ARTIFACTS / "browser-errors.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")
    assert not errors, errors
    assert all(checks.values()), checks
    print("Phase 9D standalone production-bundle component validation passed")


if __name__ == "__main__":
    main()
