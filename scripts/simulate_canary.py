"""Simulate canary: 100 synthetic pricing requests (lab thresholds)."""

from __future__ import annotations

import json
import sys
import time
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "pricing-service"))

from app import config  # noqa: E402
from app.pricing import calculate_quote  # noqa: E402

OUT = ROOT / "reports" / "evidence" / "canary-result.json"


def main() -> int:
    total = 100
    failures = 0
    violations = 0
    latencies: list[float] = []
    for i in range(total):
        demand = Decimal("4.20") if i % 2 == 0 else Decimal("1.50")
        start = time.perf_counter()
        try:
            quote = calculate_quote(f"RIDE-C-{i}", Decimal("12.50"), Decimal(25), demand)
            if quote["applied_multiplier"] > config.MAX_SURGE_MULTIPLIER:
                violations += 1
            if (
                demand > config.MAX_SURGE_MULTIPLIER
                and quote["applied_multiplier"] != config.MAX_SURGE_MULTIPLIER
            ):
                violations += 1
        except Exception:
            failures += 1
        latencies.append((time.perf_counter() - start) * 1000)
    latencies.sort()
    p95 = latencies[int(0.95 * len(latencies)) - 1]
    error_rate = failures / total
    decision = "promote" if (error_rate < 0.01 and p95 < 300 and violations == 0) else "rollback"
    result = {
        "requests": total,
        "successes": total - failures,
        "failures": failures,
        "error_rate": error_rate,
        "p95_latency_ms": round(p95, 3),
        "pricing_policy_violations": violations,
        "policy": str(config.MAX_SURGE_MULTIPLIER),
        "decision": decision,
        "note": "Local lab thresholds, not production SLOs.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if decision == "promote" else 1


if __name__ == "__main__":
    sys.exit(main())
