from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_delete():
    body = {
        "patient_id": 1,
        "loinc_num": "789-8",
        "date": "2024-01-02"
    }
    r = client.post("/delete", json=body)
    assert r.status_code in (200, 404)