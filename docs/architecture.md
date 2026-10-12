# Architecture (lab)

- ride-api (out of lab scope, contract only)
- pricing-service (FastAPI, :8011): synthetic fare + cap
- allocation-service (FastAPI, :8012): synthetic driver reservation + idempotency
- notification-service (out of lab scope)

Critical: pricing-service + allocation-service. All data synthetic.
