"""Health payload helper."""

from __future__ import annotations

from . import config


def health_payload() -> dict:
    return {
        "status": "healthy",
        "service": config.SERVICE_NAME,
        "version": config.SERVICE_VERSION,
    }


def version_payload() -> dict:
    return {
        "service": config.SERVICE_NAME,
        "service_version": config.SERVICE_VERSION,
        "commit_sha": config.COMMIT_SHA,
    }
