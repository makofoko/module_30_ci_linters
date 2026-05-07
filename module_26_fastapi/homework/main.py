from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas, database

app = FastAPI(title="Culinary Book API")

async def get_db():
    async with database.SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post("/recipes", response_model=schemas.RecipeOut)
async def create_recipe(recipe: schemas.RecipeCreate, db: AsyncSession = Depends(get_db)):
    new_recipe = models.Recipe(**recipe.dict())
    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    return new_recipe

@app.get("/recipes", response_model=list[schemas.RecipeOut])
async def get_recipes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Recipe).order_by(models.Recipe.views.desc(), models.Recipe.cook_time))
    return result.scalars().all()

@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
async def get_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Recipe).where(models.Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe.views += 1
    await db.commit()
    await db.refresh(recipe)
    return recipe
