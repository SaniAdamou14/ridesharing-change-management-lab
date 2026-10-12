# ADR-001: Repository and Branching Strategy

- Decision: multi-repo-style layout in one lab repo (per-service folders +
  platform-contracts + platform-deployment equivalents) + GitHub Flow.
- Rationale: independent pipelines/releases, clear ownership, short-lived
  branches avoid long merge pain for frequent releases.
- Trade-off: coordinated changes harder → mitigated by central contracts,
  contract tests, CODEOWNERS, release dashboard, ADRs.
