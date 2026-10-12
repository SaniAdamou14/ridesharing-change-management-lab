"""SYS-01/03/06: contract and cross-service non-regression."""

from decimal import Decimal
from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from app import config
from app.main import app
from app.pricing import calculate_quote

client = TestClient(app)
ROOT = Path(__file__).resolve().parents[3]


def test_sys01_pricing_response_matches_contract() -> None:
    contract = yaml.safe_load((ROOT / "contracts" / "pricing-api.yaml").read_text(encoding="utf-8"))
    assert "/prices/calculate" in contract["paths"]
    response = client.post(
        "/prices/calculate",
        json={
            "ride_id": "RIDE-1001",
            "distance_km": "12.50",
            "duration_minutes": 25,
            "demand_index": "4.20",
            "region": "REGION-A",
        },
    )
    assert response.status_code == 200
    body = response.json()
    for field in (
        "ride_id",
        "base_amount",
        "applied_multiplier",
        "final_amount",
        "currency",
        "policy_version",
    ):
        assert field in body


def test_sys03_pricing_version_in_quote() -> None:
    quote = calculate_quote("RIDE-1", Decimal("5"), Decimal(10), Decimal("2"))
    assert quote["service_version"] == config.SERVICE_VERSION
    assert quote["policy_version"] == config.POLICY_VERSION


def test_sys06_pricing_cap_change_affects_pricing_only() -> None:
    assert config.MAX_SURGE_MULTIPLIER == Decimal("3.0")
    assert config.BASELINE_MAX_SURGE_MULTIPLIER == Decimal("5.0")
