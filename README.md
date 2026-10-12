# ridesharing-change-management-lab

Evidence lab for Unit 7: controlled change CR-2026-007 (cap surge 5.0 → 3.0).

- `services/pricing-service` :8011, v1.1.0, policy 2026.10.1
- `services/allocation-service` :8012, v1.0.0
- Synthetic data only. See docs/, traceability/, reports/evidence/.

Quick start:
`pip install -r services/pricing-service/requirements.txt`
`pytest services/pricing-service/tests -q`
`pytest services/allocation-service/tests -q`
`python scripts/verify_configuration.py`
`python scripts/simulate_canary.py`
