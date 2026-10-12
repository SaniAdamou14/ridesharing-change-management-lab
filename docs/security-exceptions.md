# Security exception — Trivy HIGH findings on base image (EXP-2026-001)

Date: 2026-10-12. Applies to: `pricing-service:1.1.0`, `allocation-service:1.0.0`.

## Finding
Trivy image scans (CI, Trivy v0.75.0) report **0 Critical, 47 HIGH** on both
images. Filesystem scan: clean. 44 of 47 HIGH affect Debian base packages
(`bsdutils`, `libblkid1`, `libacl1`, … — e.g. CVE-2026-76642, CVE-2026-78408)
with **no fixed version available** in `python:3.12-slim`; 3 have upstream
fixes pending base-image refresh.

## Severity
High (base OS packages only; no application-layer CVE in project code).

## Reason for exception
No vendor fix published for 44/47 at scan time; rebuilding on a newer digest
is the only remediation and is scheduled, not immediate.

## Risk
Low in lab context: images run as non-root `appuser`, read-only root
filesystem, explicit health checks, no embedded secrets, no reachable
exploit path demonstrated for these util-linux CVEs in this workload.

## Mitigation
Non-root user, read-only FS, resource limits, secret-free images, monthly
base-image refresh + rescan, Dependabot-style rebuild on new `python:3.12-slim`.

## Owner
Service Owner (@SaniAdamou14).

## Expiration
2026-11-12 (rescan required; exception lapses if any Critical appears).

## Approval
Service Owner + QA Reviewer (recorded in CR-2026-007 closure).
