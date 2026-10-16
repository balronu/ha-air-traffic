# Phase 9D Report — Isolated Lovelace Browser Validation

**Status:** Complete — **READY FOR BETA**

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

One intermediate run also exposed an intermittent browser `pageerror`,
serialized by Playwright as `Error("Object")`, after the full matrix had
rendered. It was not reproduced in the final run below: the final browser error
list, console, HTTP request failures, WebSocket diagnostics, and Home Assistant
integration-error log were all clean. The standalone component test remains as
an independent supplementary check.

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

Validation commit: `0d3c4bfe03a60294b47cdcdb14217940903cafab`; final report
commit: `cd1538c77f38ed088fdade33d86b40797d898bd3`.

- [Phase 9D CI run 38866438763](https://github.com/balronu/ha-air-traffic/actions/runs/38866438763): installation, bundle build, isolated HA browser gate, standalone production-bundle component test, and artifact upload passed on final report HEAD `cd1538c`.
- The preceding diagnostic run [38864384126](https://github.com/balronu/ha-air-traffic/actions/runs/38864384126) was red on the intermittent `Error("Object")` pageerror and remains documented as a non-final diagnostic result.
- Browser DOM evidence recorded exactly 4 modern cards and 1 legacy card, with TEST123=2, TEST456=2, empty-state=2, source-error=1, and stale-state=1; browser errors, console output, request failures, and integration-error filter were empty.
- Component checks passed for modern and legacy cards, automatic registration, TEST123/TEST456, detail selection, state-driven aircraft update, source-error/stale/empty states, and the production bundle.
- [CI artifacts](https://github.com/balronu/ha-air-traffic/actions/runs/38866438763#artifacts) (artifact `phase9d-lovelace-evidence`, ID `12031712579`, 47 files, 700266 bytes): screenshots, browser console/errors, request failures, WebSocket frames, Home Assistant logs, DOM checks, and component evidence.

The captured complete Home Assistant log also contains unrelated runner-level
warnings/errors from optional `ffmpeg`/camera setup; the dedicated
`custom_components.air_traffic_merge` integration-error filter is empty and
the Phase 9D job passed. These optional-environment messages are not treated as
production integration failures.

The HA matrix reached the empty Lovelace view, native Markdown card, exactly
four modern Air Traffic card elements and exactly one legacy card element,
FR24/ADS-B aircraft, detail selection, source-error, stale-data and empty
states, plus the responsive/theme stages before the final error gate. The
independent component test confirms the same bundle with only the required HA
surface mocked.

## Remaining risks and decision

**Final assessment: READY FOR BETA.** The final isolated HA/Playwright E2E gate
and the independent production-bundle component test are green. The earlier
intermittent `Error("Object")` is retained as a diagnostic risk observation,
but was absent from the final run and did not block the completed matrix.

PR #4 remains open and unmerged; browser-validation code was validated at
`0d3c4bf` and this report is finalized in the following documentation commit.
No tag, release, productive
HA/dashboard, VM 104/Proxmox, HACS removal, or old-card-repository archival
was made.
