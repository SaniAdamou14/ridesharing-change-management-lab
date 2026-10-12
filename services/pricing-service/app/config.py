"""Runtime configuration for pricing-service (synthetic lab values only)."""

from __future__ import annotations

import os
from decimal import Decimal


def _get_env(name: str, default: str) -> str:
    return os.getenv(name, default)


SERVICE_NAME: str = _get_env("SERVICE_NAME", "pricing-service")
SERVICE_VERSION: str = _get_env("SERVICE_VERSION", "1.1.0")
POLICY_VERSION: str = _get_env("POLICY_VERSION", "2026.10.1")
CURRENCY: str = _get_env("CURRENCY", "USD")

BASE_FARE: Decimal = Decimal(_get_env("BASE_FARE", "2.50"))
PRICE_PER_KM: Decimal = Decimal(_get_env("PRICE_PER_KM", "1.20"))
PRICE_PER_MINUTE: Decimal = Decimal(_get_env("PRICE_PER_MINUTE", "0.25"))
MAX_SURGE_MULTIPLIER: Decimal = Decimal(_get_env("MAX_SURGE_MULTIPLIER", "3.0"))

# Baseline (pre-change) reference, kept for audit/rollback evidence (CR-2026-007).
BASELINE_MAX_SURGE_MULTIPLIER: Decimal = Decimal("5.0")
BASELINE_SERVICE_VERSION: str = "1.0.0"
BASELINE_POLICY_VERSION: str = "2026.10.0"

COMMIT_SHA: str = _get_env("COMMIT_SHA", "local")


def public_config() -> dict:
    """Return only non-sensitive public configuration."""
    return {
        "currency": CURRENCY,
        "policy_version": POLICY_VERSION,
        "maximum_surge_multiplier": str(MAX_SURGE_MULTIPLIER),
    }
