# Phase 9 – Controlled publication report

**Date:** 2026-10-15  
**Result:** **PUBLICATION BLOCKED**

## Completed

- PR #1 was updated with the actual validation result and merged normally.
- Merge commit: `c4c3aa3c6a2c696dd436a092c6c0408e7c116e43`
- Post-merge Tests run: [38692597308](https://github.com/balronu/ha-air-traffic/actions/runs/38692597308) — passed
- Post-merge Validate run: [38692597357](https://github.com/balronu/ha-air-traffic/actions/runs/38692597357) — passed
- Repository renamed in place from `balronu/air-traffic-merge` to
  `balronu/ha-air-traffic`; no second repository was created.
- Local `origin` was updated to `https://github.com/balronu/ha-air-traffic.git`.
- GitHub description and prepared topics were set.
- The obsolete public README status was corrected in PR #2 and merged as
  `2c379dc542de657ce79a39f9d7d512e4b37e4a4e`.
- The old card repository remains unchanged and unarchived.

## GitHub metadata and assets

- Description: `Home Assistant air traffic integration with built-in Lovelace card`
- Topics: `air-traffic`, `ads-b`, `aircraft`, `aviation`, `hacs`,
  `home-assistant`, `home-assistant-custom-component`, `lovelace`,
  `flightradar24`
- README logo and banner are reachable from `main`.
- Social Preview asset is present in the repository at 1280 × 640 pixels.
- Social Preview was **not uploaded to GitHub settings** because the available
  browser session was not authenticated for repository settings. Manual upload
  remains required; this was not the publication blocker.
- No local `brand/icon.png` was created. The existing project asset is not
  automatically used as Home Assistant local integration branding, and no
  separate brand file was added without a verified requirement.

## API, redirect and Raw checks

- New GitHub API repository: reachable, public, non-archived.
- Old repository URL redirects to `balronu/ha-air-traffic`.
- Raw manifest: HTTP 200.
- Raw bundled frontend: HTTP 200.
- Raw English README: HTTP 200.
- Raw social-preview PNG: HTTP 200.
- Manifest domain remains `air_traffic_merge`.
- The old card repository `balronu/air-traffic-merge-card` remains public and
  unarchived.

## HACS check

The read-only Home Assistant HACS inspection found the existing installation
under the old repository ID:

- HACS repository ID: `balronu/air-traffic-merge`
- Resolved full name: `balronu/ha-air-traffic`
- Installed version: `v1.3.1`
- Domain: `air_traffic_merge`
- `can_download`: true
- Current available version: `v1.3.1`

This shows that the existing installation follows the GitHub rename and keeps
the technical domain. The HACS central search index does not yet list
`balronu/ha-air-traffic`, and the new repository has no beta release yet.
Therefore HACS beta discovery/update behavior cannot be proven before a tag and
release exist. No HACS add, install, update, restart, or productive HA change
was performed.

## Isolated Lovelace test

The required isolated browser test was **not executable** in this environment:

- Docker unavailable
- Podman unavailable
- `hass` executable unavailable
- Python `homeassistant` package unavailable
- No isolated HA instance was listening on port 8123

The remote frontend tests/build verify the bundle contract, but they do not
replace an interactive Home Assistant browser test for automatic resource
registration, both card types, legacy parameters, `max_items: 25`, selection,
detail view, responsive layout, cache versioning, and reload behavior.

## Release state

- `v1.4.0-beta.1` tag: **not created**
- GitHub beta release: **not created**
- Release artifacts: **not applicable yet**
- Old card repository archive/delete: **not performed**
- Productive Home Assistant, dashboard, entity and Proxmox changes: **none**

## Required continuation

1. Provide or start an isolated Home Assistant test environment.
2. Run the browser matrix documented in Phase 9.
3. Re-check HACS after the beta tag/release exists, without modifying the
   productive installation.
4. Upload the prepared Social Preview manually through GitHub settings.
5. Only after those gates pass, create and push `v1.4.0-beta.1`, publish the
   pre-release with the prepared release notes, and verify HACS update behavior.

Until then, publication remains blocked by the missing isolated Lovelace test.
