from typing import cast
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from module_30_ci_linters.homework.hw1 import models, schemas
from module_30_ci_linters.homework.hw1.database import SessionLocal

# 1. СНАЧАЛА создаем роутер
router = APIRouter(prefix="/recipes", tags=["recipes"])

# 2. ОПРЕДЕЛЯЕМ зависимости
async def get_db():
    async with SessionLocal() as session:
        yield session

# 3. ТОЛЬКО ТЕПЕРЬ используем декораторы @router
@router.get("/", response_model=list[schemas.RecipeOut])
async def get_recipes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Recipe).order_by(
            models.Recipe.views.desc(),
            models.Recipe.cook_time,
        )
    )
    return result.scalars().all()

@router.get("/{recipe_id}", response_model=schemas.RecipeOut)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    recipe = result.scalar_one()
    # Исправление для mypy
    recipe.views = cast(int, recipe.views) + 1
    await db.commit()
    await db.refresh(recipe)
    return recipe

@router.post("/", response_model=schemas.RecipeOut)
async def create_recipe(
    recipe: schemas.RecipeCreate,
    db: AsyncSession = Depends(get_db),
):
    new_recipe = models.Recipe(**recipe.dict())
    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    return new_recipe