# Phase 9D Report — Isolated Lovelace Browser Validation

**Status:** Complete — **NOT READY FOR BETA**

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

## Root cause of the remaining CI failure

The corrected fixture reaches the production bundle and renders the expected
cards and content. The latest HA browser gate failed on a test-only resource
selector that required the URL to contain `/air_traffic_merge/`; Home
Assistant's actual resource URL contains the same production filename but a
different prefix. The browser error list, request failures, WebSocket
diagnostics, and Home Assistant integration-error log were empty.

An earlier assertion failure was another test-only defect: the legacy card is
registered as `air-traffic-merge-card`, so the page contains four modern card
elements plus one legacy element. The test now checks those separately.

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

Validation commit: `1a1fdb8cff67b0fb78a38df816e1a7b743120db2`.

- [Phase 9D CI run 38733133101](https://github.com/balronu/ha-air-traffic/actions/runs/38733133101): installation and bundle build passed; isolated HA browser gate failed on the single page error; standalone production-bundle component test passed.
- Component checks passed for modern and legacy cards, automatic registration, TEST123/TEST456, detail selection, empty/error/stale states, and the production bundle.
- [Tests run 38733133102](https://github.com/balronu/ha-air-traffic/actions/runs/38733133102): passed.
- [Validate run 38733133138](https://github.com/balronu/ha-air-traffic/actions/runs/38733133138): passed.
- [CI artifacts](https://github.com/balronu/ha-air-traffic/actions/runs/38733133101#artifacts): screenshots, browser console/errors, request failures, WebSocket frames, Home Assistant logs, DOM checks, and component evidence.

The HA matrix reached the empty Lovelace view, native Markdown card, both Air
Traffic card types, FR24/ADS-B aircraft, detail selection, source-error,
stale-data and empty states, plus the responsive/theme stages before the final
error gate. The independent component test confirms the same bundle with only
the required HA surface mocked.

## Remaining risks and decision

**Final assessment remains pending the rerun of the corrected resource selector.**
The standalone bundle test is supplementary and does not replace the HA-E2E.

PR #4 remains open and unmerged; browser-validation code was validated at
`1a1fdb8` and this report was finalized in documentation commits `43b482e` and
`016f29c`. No tag, release, productive
HA/dashboard, VM 104/Proxmox, HACS removal, or old-card-repository archival
was made.
