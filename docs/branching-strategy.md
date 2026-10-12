# Branching Strategy

GitHub Flow with release tags + temporary hotfix branches.

- `main`: always deployable, protected, no direct push, CI required, ≥1 review.
- `feature/CR-ID-description`: short-lived, e.g. `feature/CR-2026-007-surge-cap`.
- `fix/ISSUE-ID-description`: e.g. `fix/ISSUE-143-driver-timeout`.
- `hotfix/INC-ID-description`: e.g. `hotfix/INC-2026-011-duplicate-allocation`.

Versioning: MAJOR.MINOR.PATCH (`pricing-service-v1.1.0`).
Conventional commits: feat, fix, docs, test, refactor, chore, ci, perf, revert.
