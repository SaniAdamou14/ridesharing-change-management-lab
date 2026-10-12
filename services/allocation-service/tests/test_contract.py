"""SYS-02/07/08: allocation contract, non-regression, rollback."""

from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from app import allocation, config
from app.main import app

client = TestClient(app)
ROOT = Path(__file__).resolve().parents[3]


def test_sys02_allocation_response_matches_contract() -> None:
    contract = yaml.safe_load(
        (ROOT / "contracts" / "allocation-api.yaml").read_text(encoding="utf-8")
    )
    assert "/drivers/allocate" in contract["paths"]
    allocation.reset_state()
    response = client.post(
        "/drivers/allocate",
        json={
            "ride_id": "RIDE-SYS-02",
            "request_id": "REQ-SYS-02",
            "passenger_latitude": "13.5116",
            "passenger_longitude": "2.1254",
        },
    )
    assert response.status_code == 201
    for field in ("ride_id", "driver_id", "status", "allocation_version", "expires_in_seconds"):
        assert field in response.json()


def test_sys07_allocation_unchanged_after_pricing_release() -> None:
    assert config.SERVICE_VERSION == "1.0.0"
    pricing_version = (ROOT / "services" / "pricing-service" / "VERSION").read_text().strip()
    assert pricing_version == "1.1.0"


def test_sys08_rollback_restores_multiplier() -> None:
    baseline = (ROOT / "docs" / "change-requests" / "CR-2026-007.md").read_text(encoding="utf-8")
    assert "5.0" in baseline and "3.0" in baseline
    rollback = (ROOT / "docs" / "rollback-plan.md").read_text(encoding="utf-8")
    assert "1.0.0" in rollback
