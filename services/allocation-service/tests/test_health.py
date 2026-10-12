"""ALC-01/02: health and version endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_healthy() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_version_endpoint() -> None:
    response = client.get("/version")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "allocation-service"
    assert body["service_version"] == "1.0.0"
