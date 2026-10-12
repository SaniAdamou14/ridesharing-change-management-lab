# Release evidence — pricing-service v1.1.0 (CR-2026-007)

- Change: cap MAX_SURGE_MULTIPLIER 5.0 → 3.0; policy 2026.10.0 → 2026.10.1.
- Release: https://github.com/SaniAdamou14/ridesharing-change-management-lab/releases/tag/pricing-service-v1.1.0
- Tagged commit: `b8ab8c4eec6b27ee4a9e8d75ed83b00e0f21053b` (tag moved twice with
  `-f` during the lab: first to pick up the fixed release workflow, then the
  `.gitkeep` upload fix — documented here instead of hidden).

## CI results (GitHub Actions, Python 3.12)
- PR #1 (CI upgrade): https://github.com/SaniAdamou14/ridesharing-change-management-lab/pull/1 — run 38226175046 ✅
- PR #2 (release-upload fix): https://github.com/SaniAdamou14/ridesharing-change-management-lab/pull/2 — run 38226810559 ✅
- Release run: 38227107115 ✅ (tests + gates + scans + SBOM + canary/rollback sims, GH Release published)
- Audit runs: 38225785460 ✅, 38226473018 ✅
- Tests (CI): pricing 18/18, allocation 21/21, 0 failed, 0 skipped.
- Coverage (CI): pricing 100% stmt / 100% branch; allocation 99.3% / 93.3%.
- Config audit: 24/24. Traceability: passed. Smoke: passed.
- Canary: 100 requests, 0 failures, 0 policy violations → promote.
- Rollback simulation: passed (target v1.0.0, allocation unchanged).

## Images (CI digests)
- pricing-service:1.1.0 `sha256:5ccec8366bd2157001907c5c6a16f9afc965d52204bd8ccc0d649ce049f7d0f1`
- allocation-service:1.0.0 (same base; see PR artifact `unit7-pr-evidence`)
- Non-root `appuser`, health checks, `python:3.12-slim`, Compose verified live.

## Security
- Trivy (v0.75.0, CI): filesystem clean; images 0 Critical / 47 HIGH
  (44 without upstream fix at scan time).
- Documented exception: `docs/security-exceptions.md` (EXP-2026-001).
- SBOM: SPDX-2.3, 116 packages (`release-sbom.spdx.json`).

## Baseline reference
Pre-change cap 5.0 preserved as `BASELINE_MAX_SURGE_MULTIPLIER` + PRC-13 test.
