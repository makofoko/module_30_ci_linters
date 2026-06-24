import pytest
from httpx import AsyncClient
from .main import app

@pytest.mark.asyncio
async def test_create_recipe():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/recipes", json={
            "title": "Борщ",
            "cook_time": 60,
            "ingredients": "Свекла, капуста, мясо",
            "description": "Классический рецепт борща"
        })
    assert response.status_code == 200
    assert response.json()["title"] == "Борщ"

@pytest.mark.asyncio
async def test_get_recipes():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
