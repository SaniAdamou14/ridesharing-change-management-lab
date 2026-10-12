"""FastAPI entrypoint for pricing-service."""

from __future__ import annotations

from decimal import Decimal

from fastapi import FastAPI, HTTPException

from . import config
from .health import health_payload, version_payload
from .models import PriceRequest
from .pricing import calculate_quote

app = FastAPI(title="pricing-service", version=config.SERVICE_VERSION)


@app.get("/health")
def get_health() -> dict:
    return health_payload()


@app.get("/version")
def get_version() -> dict:
    return version_payload()


@app.get("/config")
def get_config() -> dict:
    return config.public_config()


@app.post("/prices/calculate")
def calculate_price(body: PriceRequest) -> dict:
    try:
        result = calculate_quote(
            ride_id=body.ride_id,
            distance_km=Decimal(body.distance_km),
            duration_minutes=Decimal(body.duration_minutes),
            demand_index=Decimal(body.demand_index),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    # Serialize Decimals as strings to preserve precision over JSON.
    return {
        "ride_id": result["ride_id"],
        "base_amount": str(result["base_amount"]),
        "requested_multiplier": str(result["requested_multiplier"]),
        "applied_multiplier": str(result["applied_multiplier"]),
        "final_amount": str(result["final_amount"]),
        "currency": result["currency"],
        "service_version": result["service_version"],
        "policy_version": result["policy_version"],
        "capped": result["capped"],
    }
