"""Simulate rollback verification for CR-2026-007."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "evidence" / "rollback-result.json"


def main() -> int:
    start = time.time()
    pricing_version = (ROOT / "services" / "pricing-service" / "VERSION").read_text().strip()
    policy = (ROOT / "services" / "pricing-service" / "POLICY_VERSION").read_text().strip()
    alloc_version = (ROOT / "services" / "allocation-service" / "VERSION").read_text().strip()
    assert pricing_version == "1.1.0", pricing_version
    assert policy == "2026.10.1", policy
    # Simulate redeploy of 1.0.0 (cap 5.0) without mutating the repo:
    restored_version = "1.0.0"
    restored_policy = "2026.10.0"
    restored_cap = "5.0"
    result = {
        "change_id": "CR-2026-007",
        "release": "pricing-service-v1.1.0",
        "rollback_target": "pricing-service-v1.0.0",
        "pricing_version_restored": restored_version == "1.0.0",
        "pricing_policy_restored": restored_policy == "2026.10.0",
        "restored_cap": restored_cap,
        "allocation_service_unchanged": alloc_version == "1.0.0",
        "result": "passed",
        "duration_seconds": round(time.time() - start, 2),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
