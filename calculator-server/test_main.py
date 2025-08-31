from fastapi.testclient import TestClient
from main import app  # or whatever your app module is
# import models

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", json={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", json={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", json={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", json={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""


"""Add more tests"""
def test_multiplication_symbol():
    r = client.post("/calculate", json={"expr": "30×4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 120) < 1e-9

def test_division_symbol():
    r = client.post("/calculate", json={"expr": "30÷4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_basic_addition():
    r = client.post("/calculate", json={"expr": "30+4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 34) < 1e-9

def test_basic_subtraction():
    r = client.post("/calculate", json={"expr": "22-50"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - (-28)) < 1e-9

def test_multiple_percent():
    r = client.post("/calculate", json={"expr": "6%%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.0006) < 1e-9

def test_get_empty_history():
    r = client.delete("/history")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["cleared"] is True
    r = client.get("/history")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 0

def test_get_three_history():
    r = client.delete("/history")
    assert r.status_code == 200
    for expr in ["6%", "100 - 6%", "30/4"]:
        r = client.post("/calculate", json={"expr": expr})
        assert r.status_code == 200
        data = r.json()
        assert data["ok"] is True

    r = client.get("/history")
    assert r.status_code == 200
    h = r.json()
    assert len(h) == 3
    expected = [("30/4", 7.5), ("100 - 6%", 94.0), ("6%", 0.06)]
    for i, (expr, result) in enumerate(expected):
        entry = h[i]
        assert entry["expr"] == expr
        assert abs(entry["result"] - result) < 1e-9
        assert entry["ok"] is True
        assert entry["error"] == ""
