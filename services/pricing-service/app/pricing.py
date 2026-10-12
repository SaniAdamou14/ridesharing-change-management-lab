"""Synthetic fare computation. No real commercial pricing logic."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from . import config

TWOPLACES = Decimal("0.01")


def quantize(value: Decimal) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


def compute_base(distance_km: Decimal, duration_minutes: Decimal) -> Decimal:
    if distance_km < 0:
        raise ValueError("distance_km must be >= 0")
    if duration_minutes < 0:
        raise ValueError("duration_minutes must be >= 0")
    raw = (
        config.BASE_FARE
        + distance_km * config.PRICE_PER_KM
        + duration_minutes * config.PRICE_PER_MINUTE
    )
    return quantize(raw)


def apply_cap(demand_index: Decimal, max_surge: Decimal | None = None) -> Decimal:
    cap = config.MAX_SURGE_MULTIPLIER if max_surge is None else max_surge
    if demand_index < Decimal("1"):
        raise ValueError("demand_index must be >= 1")
    applied = demand_index if demand_index <= cap else cap
    return quantize(applied)


def calculate_quote(
    ride_id: str,
    distance_km: Decimal,
    duration_minutes: Decimal,
    demand_index: Decimal,
    max_surge: Decimal | None = None,
) -> dict:
    base = compute_base(distance_km, duration_minutes)
    requested = quantize(demand_index)
    applied = apply_cap(demand_index, max_surge)
    final = quantize(base * applied)
    capped = applied < requested
    return {
        "ride_id": ride_id,
        "base_amount": base,
        "requested_multiplier": requested,
        "applied_multiplier": applied,
        "final_amount": final,
        "currency": config.CURRENCY,
        "service_version": config.SERVICE_VERSION,
        "policy_version": config.POLICY_VERSION,
        "capped": capped,
    }
