"""Smoke test both services via TestClient (no Docker required)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "services" / "pricing-service"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "services" / "allocation-service"))

import importlib.util  # noqa: E402


def load_app(service: str):
    base = Path(__file__).resolve().parents[1] / "services" / service
    spec = importlib.util.spec_from_file_location(f"{service}_main", base / "app" / "main.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"{service}_main"] = module
    spec.loader.exec_module(module)
    return module.app


def main() -> int:
    out = Path(__file__).resolve().parents[1] / "reports" / "evidence" / "smoke-test.json"
    results: dict = {"checks": []}

    def check(name: str, ok: bool) -> None:
        results["checks"].append({"name": name, "passed": ok})
        if not ok:
            print(f"SMOKE FAIL: {name}")

    # Pricing via direct import (isolated sys.path handling below).
    import subprocess

    for service, port in (("pricing-service", 8011), ("allocation-service", 8012)):
        code = (
            "from fastapi.testclient import TestClient; import sys; "
            f"sys.path.insert(0, 'services/{service}'); "
            "from app.main import app; c=TestClient(app); "
            "r=c.get('/health'); print(r.status_code, r.json())"
        )
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).resolve().parents[1]),
        )
        check(f"{service} /health", proc.returncode == 0 and "healthy" in proc.stdout)

    results["result"] = "passed" if all(c["passed"] for c in results["checks"]) else "failed"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return 0 if results["result"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
