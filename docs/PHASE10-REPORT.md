# Phase 10 Report — Air Traffic v1.4.0-beta.1

**Result:** Published as a GitHub pre-release. No stable release was created.

## Merge and validation

- PR: [#4](https://github.com/balronu/ha-air-traffic/pull/4)
- Merge commit: `137a3ee8a1712b4008304d431293e119b32e3157`
- Main Tests: [run 38871068479](https://github.com/balronu/ha-air-traffic/actions/runs/38871068479)
- Main Validate: [run 38871068453](https://github.com/balronu/ha-air-traffic/actions/runs/38871068453)
- Phase 9D browser gate: [run 38868720577](https://github.com/balronu/ha-air-traffic/actions/runs/38868720577)

Both post-merge Main workflows passed before release preparation. The tested
candidate preserves the internal `air_traffic_merge` domain, existing entity
and unique-ID contracts, Config Entries, and the legacy
`custom:air-traffic-merge-card` type. The browser fixture validates the
Home-Assistant slug `sensor.ads_b_feed`, both card types, automatic registration,
aircraft selection/update, source-error/stale/empty states and responsive/theme
rendering. No unintended production integration files were changed by PR #4;
its diff is limited to CI validation scripts and reports.

## Version and release

- Version: `1.4.0-beta.1`
- Tag: `v1.4.0-beta.1`
- GitHub pre-release: https://github.com/balronu/ha-air-traffic/releases/tag/v1.4.0-beta.1
- Stable release: **not created**

The version is consistent in the integration manifest, `pyproject.toml`,
frontend `package.json`, and `package-lock.json`. The annotated tag is created
only on the CI-verified Main release-preparation commit.

## HACS result

The repository remains publicly reachable and contains the required
`hacs.json`, manifest, README and versioned frontend bundle. The published
GitHub pre-release is discoverable by HACS when beta/pre-release visibility is
enabled (`show_beta`); existing installations are not modified and no HACS
storage or Home Assistant action was performed.

## Remaining risks and boundaries

- This is a beta; the legacy card remains for compatibility and old Lovelace
  resources should only be removed after an installation-specific check.
- HACS beta visibility depends on the user's `show_beta` setting.
- The isolated runner emitted unrelated optional ffmpeg/camera warnings; the
  Air Traffic integration error filter was empty and all required gates passed.
- No automatic Home Assistant installation/update, dashboard change, VM 104,
  Proxmox, or old-card-repository archival was performed.
