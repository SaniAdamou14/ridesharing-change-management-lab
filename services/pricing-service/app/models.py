"""Pydantic models for pricing-service."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field


class PriceRequest(BaseModel):
    ride_id: str = Field(min_length=1)
    distance_km: Decimal
    duration_minutes: Decimal
    demand_index: Decimal
    region: str = Field(min_length=1)


class PriceResponse(BaseModel):
    ride_id: str
    base_amount: Decimal
    requested_multiplier: Decimal
    applied_multiplier: Decimal
    final_amount: Decimal
    currency: str
    service_version: str
    policy_version: str
    capped: bool


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class VersionResponse(BaseModel):
    service: str
    service_version: str
    policy_version: str
    commit_sha: str


class PublicConfigResponse(BaseModel):
    currency: str
    policy_version: str
    maximum_surge_multiplier: str
