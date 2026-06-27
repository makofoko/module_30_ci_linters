from fastapi.testclient import TestClient

from module_30_ci_linters.homework.hw1.app import app

client = TestClient(app)


def test_get_recipes_empty():
    response = client.get("/recipes/")
    assert response.status_code == 200
    assert response.json() == []
