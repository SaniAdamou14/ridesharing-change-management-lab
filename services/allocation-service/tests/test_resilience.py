"""ALC extra branch coverage: expiry reallocation and release paths."""

from fastapi.testclient import TestClient

from app import allocation
from app.main import app

client = TestClient(app)


def setup_function(_: object) -> None:
    allocation.reset_state()


def test_reallocate_same_ride_after_expiry() -> None:
    client.post(
        "/drivers/allocate",
        json={
            "ride_id": "RIDE-REEXP",
            "request_id": "REQ-REEXP-1",
            "passenger_latitude": "13.5",
            "passenger_longitude": "2.1",
        },
    )
    allocation.force_expire("RIDE-REEXP")
    response = client.post(
        "/drivers/allocate",
        json={
            "ride_id": "RIDE-REEXP",
            "request_id": "REQ-REEXP-2",
            "passenger_latitude": "13.5",
            "passenger_longitude": "2.1",
        },
    )
    assert response.status_code == 201


def test_same_request_id_after_expiry_reallocates() -> None:
    payload = {
        "ride_id": "RIDE-REIDEM",
        "request_id": "REQ-REIDEM",
        "passenger_latitude": "13.5",
        "passenger_longitude": "2.1",
    }
    client.post("/drivers/allocate", json=payload)
    allocation.force_expire("RIDE-REIDEM")
    response = client.post("/drivers/allocate", json=payload)
    assert response.status_code == 201


def test_invalid_longitude_rejected() -> None:
    response = client.post(
        "/drivers/allocate",
        json={
            "ride_id": "RIDE-BADLON",
            "request_id": "REQ-BADLON",
            "passenger_latitude": "13.5",
            "passenger_longitude": "250.0",
        },
    )
    assert response.status_code == 422


def test_release_unknown_ride_controlled_error() -> None:
    response = client.post("/drivers/release", json={"ride_id": "RIDE-NOPE"})
    assert response.status_code == 404
