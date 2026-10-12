"""Pydantic models for allocation-service."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field


class AllocateRequest(BaseModel):
    ride_id: str = Field(min_length=1)
    request_id: str = Field(min_length=1)
    passenger_latitude: Decimal
    passenger_longitude: Decimal


class ReleaseRequest(BaseModel):
    ride_id: str = Field(min_length=1)


class AllocationResponse(BaseModel):
    ride_id: str
    driver_id: str
    status: str
    allocation_version: str
    expires_in_seconds: int
