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
cards and content. Earlier red runs were test-harness defects: the HA-slugged
ADS-B entity was initially referenced incorrectly; the legacy card is a
separate `air-traffic-merge-card` element; and dynamic HA resource loading made
script/Performance-Entry/response selectors unstable. Those assertions were
removed or corrected without weakening the rendered-card checks.

The final HA browser run reaches the complete matrix and then fails only on one
browser `pageerror`, serialized by Playwright as `Error("Object")`. Its source
cannot be localized from the browser event, while the captured browser console,
HTTP request failures, WebSocket diagnostics, and Home Assistant integration
error log contain no corresponding failure. This is an unresolved real-browser
E2E gap, not a successful E2E result. The standalone component test remains a
supplementary fallback and does not replace this gate.

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

Validation commit: `a5578b4420457edf19cfb60c867f5a0459d65ecb`.

- [Phase 9D CI run 38864384126](https://github.com/balronu/ha-air-traffic/actions/runs/38864384126): installation and bundle build passed; the isolated HA browser gate failed only on the unresolved `Error("Object")` pageerror; the standalone production-bundle component test passed.
- Component checks passed for modern and legacy cards, automatic registration, TEST123/TEST456, detail selection, state-driven aircraft update, source-error/stale/empty states, and the production bundle.
- [Tests run 38864384132](https://github.com/balronu/ha-air-traffic/actions/runs/38864384132): passed.
- [Validate run 38864384130](https://github.com/balronu/ha-air-traffic/actions/runs/38864384130): passed.
- [CI artifacts](https://github.com/balronu/ha-air-traffic/actions/runs/38864384126#artifacts): screenshots, browser console/errors, request failures, WebSocket frames, Home Assistant logs, DOM checks, and component evidence.

The HA matrix reached the empty Lovelace view, native Markdown card, both Air
Traffic card types, FR24/ADS-B aircraft, detail selection, source-error,
stale-data and empty states, plus the responsive/theme stages before the final
error gate. The independent component test confirms the same bundle with only
the required HA surface mocked.

## Remaining risks and decision

**Final assessment: NOT READY FOR BETA.** The production bundle and fallback
component test are green, but the real HA/Playwright E2E gate is red because of
the unresolved browser `pageerror`. The remaining risk is therefore explicit:
the integrated HA browser path is not yet proven clean.

PR #4 remains open and unmerged; browser-validation code was validated at
`a5578b4` and this report is finalized in the following documentation commit.
No tag, release, productive
HA/dashboard, VM 104/Proxmox, HACS removal, or old-card-repository archival
was made.
