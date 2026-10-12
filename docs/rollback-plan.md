# Rollback Plan (CR-2026-007)

1. Detect breach via canary/monitoring.
2. Contain: halt promotion, keep v1.0.0 digest ready.
3. Redeploy `pricing-service:1.0.0` by digest (MAX_SURGE 5.0).
4. Verify /version, /config, smoke quote, allocation unchanged.
5. Reconcile affected quotes; record in reports/evidence/rollback-result.json.
