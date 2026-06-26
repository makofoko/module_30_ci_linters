import pytest
from httpx import AsyncClient
from app import app

@pytest.mark.asyncio
async def test_create_recipe():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/recipes/", json={
            "title": "Борщ",
            "cook_time": 60,
            "ingredients": "свекла, капуста, мясо",
            "description": "Классический борщ"
        })
    assert response.status_code == 200
    assert response.json()["title"] == "Борщ"
