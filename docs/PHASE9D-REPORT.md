# Phase 9D Report — Isolated Lovelace Browser Validation

**Status:** Pending CI execution on the updated PR head.

## Scope and isolation

Phase 9D runs only in a temporary GitHub Actions runner with Home Assistant Core
2026.10.1, the production frontend bundle, Playwright, and Chromium. It copies
the repository integration into a temporary HA configuration and never accesses
productive Home Assistant, VM 104, Proxmox, dashboards, HACS storage, tags, or
releases.

## Root cause of the previous failure

The previous browser run reached Lovelace successfully. Its first functional
assertion failed because the fixture named `ADS-B Feed` was referenced as
`sensor.adsb_feed`, while Home Assistant slugifies that name to
`sensor.ads_b_feed`. The integration therefore correctly reported an unavailable
ADS-B entity and returned no TEST123/TEST456 aircraft. The production bundle was
not the cause and had not yet reached its aircraft assertions.

## Phase 9D validation order

The updated test deliberately gates the matrix in this order:

1. Empty Lovelace view without Air Traffic elements.
2. Native Home Assistant Markdown card.
3. Real Air Traffic integration configuration and Options flow.
4. Production bundle with `custom:air-traffic-card` and legacy
   `custom:air-traffic-merge-card`, automatic resource registration, duplicate
   registration checks, `max_items: 25`, aircraft rows, detail selection,
   source error/stale/empty states, live fixture update, mobile layout, and
   light/dark themes.

The test captures screenshots, browser console errors, failed/error responses,
WebSocket frames, integration errors, and the complete Home Assistant log as
CI artifacts. Any assertion failure keeps the workflow red.

## Results

To be filled from the completed CI run: run URL, artifact URL, screenshot matrix,
console/request/WebSocket review, and final commit.

## Remaining risks and decision

The final assessment is **NOT READY FOR BETA** until the updated CI run passes
all gates and the resulting artifacts are reviewed. No tag, release, merge to
`main`, productive HA change, dashboard change, Proxmox change, HACS removal,
or old-card-repository archival is authorized by this phase.
