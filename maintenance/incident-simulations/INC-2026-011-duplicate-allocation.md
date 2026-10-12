# INC-2026-011: Duplicate Driver Allocation

- Detection: duplicate assignment rate alert.
- Impact: two rides same driver (synthetic).
- Timeline: detect → contain → fix → verify.
- Cause: two requests read same available driver before commit.
- Corrective: atomic reservation; idempotency key; optimistic concurrency.
- Preventive: reconciliation worker; regression ALC-04/ALC-06.
- CIs changed: allocation.py + tests. Rollback: redeploy prior digest.
- Owner: allocation owner. Closure: 0 duplicates in regression + canary.
