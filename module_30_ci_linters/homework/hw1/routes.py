from typing import cast

from sqlalchemy import Column, Integer

# ... остальные импорты


@router.get("/{recipe_id}", response_model=schemas.RecipeOut)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    recipe = result.scalar_one()

    # Исправление: приводим тип к int, если mypy считает, что там ColumnElement
    current_views = cast(int, recipe.views)
    recipe.views = current_views + 1

    await db.commit()
    await db.refresh(recipe)  # Рекомендуется добавить refresh после коммита
    return recipe
