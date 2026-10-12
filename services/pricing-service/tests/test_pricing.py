"""PRC-03..PRC-11: fare calculation behaviour (CR-2026-007)."""

from decimal import Decimal

from fastapi.testclient import TestClient

from app import config
from app.main import app
from app.pricing import apply_cap, calculate_quote

client = TestClient(app)


def _payload(demand: str) -> dict:
    return {
        "ride_id": "RIDE-1001",
        "distance_km": "12.50",
        "duration_minutes": 25,
        "demand_index": demand,
        "region": "REGION-A",
    }


def test_prc03_normal_fare_calculated_correctly() -> None:
    # base = 2.50 + 12.50*1.20 + 25*0.25 = 2.50+15.00+6.25 = 23.75
    # demand 1.50 below cap -> final 23.75*1.50 = 35.625 -> 35.63
    response = client.post("/prices/calculate", json=_payload("1.50"))
    assert response.status_code == 200
    body = response.json()
    assert body["base_amount"] == "23.75"
    assert body["applied_multiplier"] == "1.50"
    assert body["final_amount"] == "35.63"
    assert body["capped"] is False


def test_prc04_multiplier_below_cap_unchanged() -> None:
    response = client.post("/prices/calculate", json=_payload("2.00"))
    assert response.status_code == 200
    assert response.json()["applied_multiplier"] == "2.00"


def test_prc05_multiplier_above_cap_limited() -> None:
    response = client.post("/prices/calculate", json=_payload("4.20"))
    assert response.status_code == 200
    body = response.json()
    assert body["requested_multiplier"] == "4.20"
    assert body["applied_multiplier"] == "3.00"
    assert body["final_amount"] == "71.25"
    assert body["capped"] is True


def test_prc06_multiplier_exactly_at_cap_accepted() -> None:
    response = client.post("/prices/calculate", json=_payload("3.00"))
    assert response.status_code == 200
    body = response.json()
    assert body["applied_multiplier"] == "3.00"
    assert body["capped"] is False


def test_prc07_negative_distance_rejected() -> None:
    payload = _payload("1.50")
    payload["distance_km"] = "-1.00"
    response = client.post("/prices/calculate", json=payload)
    assert response.status_code == 422


def test_prc08_negative_duration_rejected() -> None:
    payload = _payload("1.50")
    payload["duration_minutes"] = -5
    response = client.post("/prices/calculate", json=payload)
    assert response.status_code == 422


def test_prc09_demand_below_one_rejected() -> None:
    response = client.post("/prices/calculate", json=_payload("0.90"))
    assert response.status_code == 422


def test_prc10_decimal_precision_preserved() -> None:
    first = calculate_quote("R", Decimal("1.11"), Decimal("1"), Decimal("1.11"))
    assert first["final_amount"] == (first["base_amount"] * first["applied_multiplier"]).quantize(
        Decimal("0.01")
    )
    # Ensure two decimal places in serialized output.
    response = client.post("/prices/calculate", json=_payload("1.11"))
    assert len(response.json()["final_amount"].split(".")[1]) == 2


def test_prc11_repeated_input_identical_result() -> None:
    kwargs = {
        "ride_id": "RIDE-42",
        "distance_km": Decimal("3.33"),
        "duration_minutes": Decimal("7"),
        "demand_index": Decimal("2.22"),
    }
    assert calculate_quote(**kwargs) == calculate_quote(**kwargs)


def test_prc13_baseline_cap_behaviour_documented() -> None:
    # Baseline pre-change policy (v1.0.0): cap 5.0. Verified via injected
    # engine parameter so the historical rule stays regression-tested.
    assert config.BASELINE_MAX_SURGE_MULTIPLIER == Decimal("5.0")
    assert apply_cap(Decimal("4.20"), max_surge=Decimal("5.0")) == Decimal("4.20")
    assert apply_cap(Decimal("6.00"), max_surge=Decimal("5.0")) == Decimal("5.00")


def test_prc14_changed_cap_equals_3() -> None:
    assert config.MAX_SURGE_MULTIPLIER == Decimal("3.0")
    assert config.SERVICE_VERSION == "1.1.0"
    assert config.POLICY_VERSION == "2026.10.1"
