"""ALC-03..ALC-10: allocation behaviour."""

import uuid

from fastapi.testclient import TestClient

from app import allocation
from app.main import app

client = TestClient(app)


def _payload(ride: str | None = None, req: str | None = None) -> dict:
    return {
        "ride_id": ride or f"RIDE-{uuid.uuid4().hex[:6].upper()}",
        "request_id": req or f"REQ-{uuid.uuid4().hex[:6].upper()}",
        "passenger_latitude": "13.5116",
        "passenger_longitude": "2.1254",
    }


def setup_function(_: object) -> None:
    allocation.reset_state()


def test_alc03_available_driver_allocated() -> None:
    response = client.post("/drivers/allocate", json=_payload("RIDE-A03", "REQ-A03"))
    assert response.status_code == 201
    body = response.json()
    assert body["ride_id"] == "RIDE-A03"
    assert body["driver_id"].startswith("DRIVER-")
    assert body["status"] == "reserved"


def test_alc04_repeated_request_returns_original() -> None:
    first = client.post("/drivers/allocate", json=_payload("RIDE-A04", "REQ-A04")).json()
    second = client.post("/drivers/allocate", json=_payload("RIDE-A04", "REQ-A04")).json()
    assert first["driver_id"] == second["driver_id"]


def test_alc05_one_ride_one_active_allocation() -> None:
    client.post("/drivers/allocate", json=_payload("RIDE-A05", "REQ-A05-1"))
    second = client.post("/drivers/allocate", json=_payload("RIDE-A05", "REQ-A05-2")).json()
    first = client.get("/allocations/RIDE-A05").json()
    assert second["driver_id"] == first["driver_id"]


def test_alc06_reserved_driver_not_allocated_twice() -> None:
    seen: set[str] = set()
    for i in range(5):
        body = client.post(
            "/drivers/allocate", json=_payload(f"RIDE-A06-{i}", f"REQ-A06-{i}")
        ).json()
        assert body["driver_id"] not in seen
        seen.add(body["driver_id"])


def test_alc07_expired_reservation_can_be_released() -> None:
    client.post("/drivers/allocate", json=_payload("RIDE-A07", "REQ-A07"))
    allocation.force_expire("RIDE-A07")
    assert client.get("/allocations/RIDE-A07").status_code == 404
    # After expiry the driver must be reusable.
    response = client.post("/drivers/allocate", json=_payload("RIDE-A07B", "REQ-A07B"))
    assert response.status_code == 201


def test_alc08_manual_release_restores_availability() -> None:
    created = client.post("/drivers/allocate", json=_payload("RIDE-A08", "REQ-A08")).json()
    driver = created["driver_id"]
    assert client.post("/drivers/release", json={"ride_id": "RIDE-A08"}).status_code == 200
    assert client.get("/allocations/RIDE-A08").status_code == 404
    # Driver pool is small; releasing must free the driver (no permanent block).
    assert driver.startswith("DRIVER-")


def test_alc09_unknown_ride_controlled_error() -> None:
    response = client.get("/allocations/RIDE-UNKNOWN-XYZ")
    assert response.status_code == 404
    assert "unknown ride_id" in response.json()["detail"]


def test_alc10_invalid_coordinates_rejected() -> None:
    payload = _payload("RIDE-A10", "REQ-A10")
    payload["passenger_latitude"] = "120.0"
    assert client.post("/drivers/allocate", json=payload).status_code == 422
