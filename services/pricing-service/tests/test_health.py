"""PRC-01: health endpoint returns healthy."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_healthy() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert body["service"] == "pricing-service"
