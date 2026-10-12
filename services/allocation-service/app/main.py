"""FastAPI entrypoint for allocation-service."""

from __future__ import annotations

import uuid
from decimal import Decimal

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from . import allocation, config
from .health import health_payload, version_payload
from .models import AllocateRequest, ReleaseRequest

app = FastAPI(title="allocation-service", version=config.SERVICE_VERSION)


def _correlation() -> str:
    return f"CORR-{uuid.uuid4().hex[:8].upper()}"


@app.exception_handler(Exception)
async def unhandled_handler(_, exc: Exception) -> JSONResponse:  # type: ignore[no-untyped-def]
    return JSONResponse(
        status_code=500,
        content={"detail": "internal error", "correlation_id": _correlation()},
    )


@app.get("/health")
def get_health() -> dict:
    return health_payload()


@app.get("/version")
def get_version() -> dict:
    return version_payload()


@app.post("/drivers/allocate", status_code=201)
def allocate_driver(body: AllocateRequest) -> dict:
    try:
        return allocation.allocate(
            ride_id=body.ride_id,
            request_id=body.request_id,
            lat=Decimal(body.passenger_latitude),
            lon=Decimal(body.passenger_longitude),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
            headers={"X-Correlation-Id": _correlation()},
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
            headers={"X-Correlation-Id": _correlation()},
        ) from exc


@app.post("/drivers/release")
def release_driver(body: ReleaseRequest) -> dict:
    ok = allocation.release(body.ride_id)
    if not ok:
        raise HTTPException(
            status_code=404,
            detail="unknown ride_id",
            headers={"X-Correlation-Id": _correlation()},
        )
    return {"ride_id": body.ride_id, "status": "released"}


@app.get("/allocations/{ride_id}")
def get_allocation(ride_id: str) -> dict:
    record = allocation.get_allocation(ride_id)
    if record is None:
        raise HTTPException(
            status_code=404,
            detail="unknown ride_id",
            headers={"X-Correlation-Id": _correlation()},
        )
    return record
