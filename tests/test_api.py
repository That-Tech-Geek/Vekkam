from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_health():
    assert client.get("/health").json()["status"]=="ok"

def test_architecture():
    assert client.get("/v1/architecture").json()["source_of_truth"]=="canonical_learning_ir"
