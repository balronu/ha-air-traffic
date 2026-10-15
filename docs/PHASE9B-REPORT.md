# Phase 9B Report — Isolated Lovelace Validation

**Date:** 2026-10-15  
**Repository:** `balronu/ha-air-traffic`  
**Branch / HEAD:** `test/phase9b` / `db97a84`  
**Result:** **NOT READY FOR BETA**

## Scope and isolation

The validation was implemented as GitHub Actions workflow `phase9b.yml` on a temporary
Linux runner. It installed Home Assistant Core `2026.10.1`,
`home-assistant-frontend==20260930.3`, Playwright `1.55.0`, and Chromium. The test
configuration copied only the repository integration and used mock ADS-B/FR24 template
entities. No productive Home Assistant VM, token, dashboard, Proxmox host, or old card
repository was accessed or changed.

## Checks completed

- Frontend tests and production build: passed.
- Python, Hassfest, HACS structure, and secret scan checks: passed.
- The isolated Home Assistant process started and served the onboarding UI.
- Browser evidence collection was active and produced onboarding screenshots and HA logs.

## Blocking result

The real-browser test did not reach Lovelace. HA 2026.10.1 requires interactive onboarding
before the dashboard is available. The runner reached the country-selection page, but the
`ha-combo-box` remained unset in headless Chromium despite selector, Shadow-DOM, coordinate,
and keyboard interaction attempts. Consequently no claim is made for card rendering,
resource registration, aircraft selection/detail, responsive layouts, themes, stale/error
states, reload, or position updates.

Latest failed run: [38696362739](https://github.com/balronu/ha-air-traffic/actions/runs/38696362739)  
Evidence artifact: [phase9b-lovelace-evidence](https://api.github.com/repos/balronu/ha-air-traffic/actions/artifacts/11954064853/zip)

The artifact contains the Home Assistant log and onboarding screenshots/HTML. Earlier runs
`38693686063`, `38693999613`, `38694373504`, `38694634383`, `38694895630`,
`38695142034`, `38695389355`, and `38695643039` recorded the progressive harness
diagnosis; none reached the card assertions.

## Publication status

**NOT READY FOR BETA.** No tag, GitHub release, merge to `main`, productive HA change,
dashboard change, Proxmox change, or archival/deletion of `balronu/air-traffic-merge-card`
was performed. The remaining action is to make isolated HA onboarding deterministic (or
pre-seed only the isolated test instance) and rerun the complete browser matrix, including
inspection of the resulting screenshots, console, and logs.
