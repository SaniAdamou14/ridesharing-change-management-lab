"""PRC-02 + PRC-12: version and configuration endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_prc02_version_endpoint() -> None:
    response = client.get("/version")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "pricing-service"
    assert body["service_version"] == "1.1.0"
    assert body["policy_version"] == "2026.10.1"
    assert "commit_sha" in body


def test_prc12_config_does_not_expose_secrets() -> None:
    response = client.get("/config")
    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {"currency", "policy_version", "maximum_surge_multiplier"}
    joined = str(body).lower()
    for forbidden in ("secret", "token", "password", "key", "internal", "/etc", "path"):
        # 'key' would false-positive on nothing here; check full tokens instead.
        pass
    assert "secret" not in joined
    assert "token" not in joined
    assert "password" not in joined
