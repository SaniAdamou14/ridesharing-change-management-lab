python -m pytest services/pricing-service/tests -q
python -m pytest services/allocation-service/tests -q
python scripts/verify_configuration.py
python scripts/verify_traceability.py
python scripts/simulate_canary.py
python scripts/simulate_rollback.py
