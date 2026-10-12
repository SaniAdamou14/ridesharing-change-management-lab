# Canary analysis (local lab thresholds, not production SLOs)

Send 100 synthetic pricing requests against pricing-service v1.1.0.

Promote when:

- error rate < 1%
- p95 latency < 300 ms (local controlled environment)
- 100% of above-cap requests capped at 3.0
- no result above policy maximum
- /health remains available

Otherwise roll back to pricing-service v1.0.0 by immutable image digest.
See scripts/simulate_canary.py and scripts/simulate_rollback.py.
