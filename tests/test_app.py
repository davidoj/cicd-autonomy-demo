from fastapi.testclient import TestClient

from app.main import VERSION, app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_root_reports_service_metadata():
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["service"] == "cicd-autonomy-demo"
    assert body["version"] == VERSION


def test_root_reflects_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test-env")
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["environment"] == "test-env"
