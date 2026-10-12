# Change Management Policy

Workflow: Change Request → Completeness & Classification → Impact Analysis →
Risk & Rollback Analysis → Approval → Implementation Branch → Automated
Validation → Peer Review → Staging & Acceptance → Controlled Release →
Post-Deployment Verification → Closure or Rollback.

## Classification
- Standard: pre-authorized, low risk (e.g. dashboard label).
- Normal: analysis + approval (e.g. pricing threshold change).
- Emergency: critical hotfix with retrospective (e.g. duplicate allocation).

## Approval authority
- Low risk: service owner + automated gates.
- Medium risk: service owner + QA + product owner.
- High risk: Change Control Board.
- Emergency: incident commander + service owner.

Pricing-rule changes always require additional business validation.
