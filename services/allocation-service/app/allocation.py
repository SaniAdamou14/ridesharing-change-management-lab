"""Synthetic driver allocation with idempotency and atomic reservation."""

from __future__ import annotations

import hashlib
import threading
import time
from decimal import Decimal

from . import config

_lock = threading.Lock()
# ride_id -> allocation record
_allocations: dict[str, dict] = {}
# request_id -> ride_id (idempotency)
_request_index: dict[str, str] = {}
# driver_id -> ride_id (reservation)
_reserved: dict[str, str] = {}


def reset_state() -> None:
    with _lock:
        _allocations.clear()
        _request_index.clear()
        _reserved.clear()


def _validate_coordinates(lat: Decimal, lon: Decimal) -> None:
    if not (Decimal("-90") <= lat <= Decimal("90")):
        raise ValueError("passenger_latitude out of range [-90, 90]")
    if not (Decimal("-180") <= lon <= Decimal("180")):
        raise ValueError("passenger_longitude out of range [-180, 180]")


def _pick_driver(ride_id: str) -> str:
    digest = hashlib.sha256(ride_id.encode()).hexdigest()
    start = int(digest[:8], 16) % len(config.DRIVER_POOL)
    for offset in range(len(config.DRIVER_POOL)):
        candidate = config.DRIVER_POOL[(start + offset) % len(config.DRIVER_POOL)]
        if candidate not in _reserved:
            return candidate
    raise RuntimeError("no available driver")


def _is_expired(record: dict, now: float) -> bool:
    return now >= record["expires_at"]


def allocate(ride_id: str, request_id: str, lat: Decimal, lon: Decimal) -> dict:
    _validate_coordinates(lat, lon)
    now = time.time()
    with _lock:
        # Idempotency: repeated request returns original allocation.
        if request_id in _request_index:
            existing_ride = _request_index[request_id]
            record = _allocations.get(existing_ride)
            if record is not None and not _is_expired(record, now):
                return _public(record)
            # Expired -> fall through and re-allocate.
        # One active allocation per ride.
        existing = _allocations.get(ride_id)
        if existing is not None and not _is_expired(existing, now):
            _request_index[request_id] = ride_id
            return _public(existing)
        if existing is not None and _is_expired(existing, now):
            _release_locked(ride_id)
        driver_id = _pick_driver(ride_id)
        record = {
            "ride_id": ride_id,
            "driver_id": driver_id,
            "status": "reserved",
            "allocation_version": config.SERVICE_VERSION,
            "expires_at": now + config.RESERVATION_TTL_SECONDS,
            "request_id": request_id,
        }
        _allocations[ride_id] = record
        _request_index[request_id] = ride_id
        _reserved[driver_id] = ride_id
        return _public(record)


def _public(record: dict) -> dict:
    remaining = max(0, int(record["expires_at"] - time.time()))
    return {
        "ride_id": record["ride_id"],
        "driver_id": record["driver_id"],
        "status": record["status"],
        "allocation_version": record["allocation_version"],
        "expires_in_seconds": remaining,
    }


def _release_locked(ride_id: str) -> bool:
    record = _allocations.pop(ride_id, None)
    if record is None:
        return False
    driver_id = record["driver_id"]
    if _reserved.get(driver_id) == ride_id:
        del _reserved[driver_id]
    return True


def release(ride_id: str) -> bool:
    with _lock:
        return _release_locked(ride_id)


def get_allocation(ride_id: str) -> dict | None:
    now = time.time()
    with _lock:
        record = _allocations.get(ride_id)
        if record is None:
            return None
        if _is_expired(record, now):
            _release_locked(ride_id)
            return None
        return _public(record)


def force_expire(ride_id: str) -> None:
    """Test helper: mark a reservation as expired."""
    with _lock:
        if ride_id in _allocations:
            _allocations[ride_id]["expires_at"] = time.time() - 1
