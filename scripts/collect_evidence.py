"""Collect evidence pack summary."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "reports" / "evidence"


def main() -> None:
    reg = ROOT / "maintenance" / "maintenance-register.csv"
    rows = list(csv.DictReader(reg.read_text(encoding="utf-8").splitlines()))
    by_type: dict[str, int] = {}
    for row in rows:
        by_type[row["maintenance_type"]] = by_type.get(row["maintenance_type"], 0) + 1
    summary = {
        "maintenance_entries": len(rows),
        "by_type": by_type,
        "critical": sum(1 for r in rows if r["severity"] == "critical"),
        "closed": sum(1 for r in rows if r["status"] == "closed"),
        "open": sum(1 for r in rows if r["status"] != "closed"),
    }
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "maintenance-summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
