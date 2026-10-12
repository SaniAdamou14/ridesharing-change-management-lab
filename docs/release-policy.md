# Release Policy

- Tag `pricing-service-v*` / `allocation-service-v*` triggers release workflow.
- Tag must match VERSION file; image built immutable + signed + SBOM + scanned.
- Staging → smoke + perf + e2e → canary → promotion or rollback.
- Release manifest + traceability matrix required before closure.
