"""ALC idempotency, timeout and error correlation."""

import uuid

from fastapi.testclient import TestClient

from app import allocation
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


def setup_function(_: object) -> None:
    allocation.reset_state()


def test_idempotent_retry_after_partial_state() -> None:
    payload = {
        "ride_id": "RIDE-IDEM-1",
        "request_id": "REQ-IDEM-1",
        "passenger_latitude": "13.5",
        "passenger_longitude": "2.1",
    }
    first = client.post("/drivers/allocate", json=payload)
    second = client.post("/drivers/allocate", json=payload)
    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["driver_id"] == second.json()["driver_id"]


def test_timeout_creates_controlled_failure() -> None:
    # Exhaust the synthetic pool then expect a controlled 503, not a crash.
    for i in range(10):
        client.post(
            "/drivers/allocate",
            json={
                "ride_id": f"RIDE-FULL-{i}-{uuid.uuid4().hex[:4]}",
                "request_id": f"REQ-FULL-{i}-{uuid.uuid4().hex[:4]}",
                "passenger_latitude": "13.5",
                "passenger_longitude": "2.1",
            },
        )
    overflow = client.post(
        "/drivers/allocate",
        json={
            "ride_id": "RIDE-OVERFLOW",
            "request_id": "REQ-OVERFLOW",
            "passenger_latitude": "13.5",
            "passenger_longitude": "2.1",
        },
    )
    assert overflow.status_code == 503
    assert "X-Correlation-Id" in overflow.headers or "detail" in overflow.json()


def test_error_returns_correlation_identifier() -> None:
    response = client.get("/allocations/RIDE-DOES-NOT-EXIST")
    assert response.status_code == 404
    assert "X-Correlation-Id" in response.headers
    assert response.json()["detail"] == "unknown ride_id"
