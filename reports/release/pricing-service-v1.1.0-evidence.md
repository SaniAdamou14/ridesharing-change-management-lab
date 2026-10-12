# Release evidence — pricing-service v1.1.0 (CR-2026-007)

- Change: cap MAX_SURGE_MULTIPLIER 5.0 → 3.0; policy 2026.10.0 → 2026.10.1.
- Tests: pricing 18 passed / 0 failed; allocation 21 passed / 0 failed.
- Coverage: pricing 100% statement / 100% branch; allocation 98% / 95.5%.
- Config audit: 24/24 passed. Traceability: passed. Smoke: passed.
- Canary: 100 requests, 0 failures, 0 violations → promote.
- Rollback simulation: passed (target v1.0.0, allocation unchanged).
- Images: pricing-service:1.1.0 sha256:874f9f66...; allocation-service:1.0.0 sha256:06ddfe6e...
- Note: baseline cap 5.0 preserved as BASELINE_MAX_SURGE_MULTIPLIER + PRC-13.
