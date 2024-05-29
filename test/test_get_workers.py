from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_workers():
    response = client.get("/api/workers")
    assert response.status_code == 200
    workers = response.json()
    assert all(["profession" in c for c in workers])
    assert all(["age" in c for c in workers])