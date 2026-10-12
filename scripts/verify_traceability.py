"""Verify traceability matrix completeness."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "traceability" / "traceability-matrix.csv"
OUT = ROOT / "reports" / "evidence" / "traceability-audit.json"

REQUIRED = [
    "change_id",
    "issue_id",
    "branch",
    "commit_sha",
    "pull_request",
    "affected_service",
    "test_evidence",
    "workflow_run",
    "release_tag",
    "image_digest",
    "deployment_environment",
    "approval",
    "rollback_evidence",
    "final_status",
]


def main() -> int:
    rows = list(csv.DictReader(MATRIX.read_text(encoding="utf-8").splitlines()))
    incomplete = 0
    for row in rows:
        for field in REQUIRED:
            value = (row.get(field) or "").strip()
            if not value or value.lower() == "pending":
                if field == "image_digest" and value.startswith("sha256:"):
                    continue
                incomplete += 1
                break
    result = {
        "required_fields": REQUIRED,
        "rows": len(rows),
        "complete": len(rows) - incomplete,
        "incomplete": incomplete,
        "result": "passed" if incomplete == 0 else "failed",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if incomplete == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
