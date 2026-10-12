"""Runtime configuration for allocation-service (synthetic lab values only)."""

from __future__ import annotations

import os

SERVICE_NAME: str = os.getenv("SERVICE_NAME", "allocation-service")
SERVICE_VERSION: str = os.getenv("SERVICE_VERSION", "1.0.0")
RESERVATION_TTL_SECONDS: int = int(os.getenv("RESERVATION_TTL_SECONDS", "30"))
MAX_CANDIDATES: int = int(os.getenv("MAX_CANDIDATES", "10"))
MAX_RETRY_ATTEMPTS: int = int(os.getenv("MAX_RETRY_ATTEMPTS", "3"))
COMMIT_SHA: str = os.getenv("COMMIT_SHA", "local")

# Synthetic driver pool (no real geolocation).
DRIVER_POOL: list[str] = [f"DRIVER-{i:03d}" for i in range(1, 11)]
