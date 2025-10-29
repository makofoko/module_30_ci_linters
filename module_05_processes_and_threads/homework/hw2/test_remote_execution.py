import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_timeout_exceeded(client):
    resp = client.post('/run_code', data={"code": "import time; time.sleep(3)", "timeout": 1})
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["timeout"] is True
    assert "превысило" in data["message"]


def test_invalid_data(client):
    resp = client.post('/run_code', data={"code": "print(123)", "timeout": 100})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "timeout" in data["errors"]


def test_safe_execution(client):
    resp = client.post('/run_code', data={"code": "print('Hello')", "timeout": 2})
    data = resp.get_json()
    assert resp.status_code == 200
    assert "Hello" in data["stdout"]
    assert data["timeout"] is False