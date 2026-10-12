# Configuration Items

Release = immutable combination of code + image + policy + schema + manifest.

## pricing-service v1.1.0
- source: services/pricing-service/app
- VERSION: 1.1.0 (`pricing-service:1.1.0`)
- POLICY_VERSION: 2026.10.1
- container digest: recorded in traceability/release-manifest.json (`sha256:...`)
- api-contract: 1.0.0 (contracts/pricing-api.yaml)
- pricing-policy: 2026-10-15 (MAX_SURGE 3.0)
- database-schema: 17 (no migration in CR-2026-007)
- deployment-manifest: 1.1.0 (deploy/kubernetes/base/pricing-deployment.yaml)

## allocation-service v1.0.0
- source: services/allocation-service/app
- VERSION: 1.0.0
- container digest: recorded in release manifest
- api-contract: 1.0.0

## Cross-cutting
- Dockerfiles, compose file, K8s manifests, configs per environment
- Dashboards, alerts, runbooks, rollback plan, tests
