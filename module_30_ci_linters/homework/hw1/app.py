import asyncio

from fastapi import FastAPI

from module_30_ci_linters.homework.hw1.database import Base, engine
from module_30_ci_linters.homework.hw1.routes import router


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_models())

app = FastAPI(title="Cookbook API", description="API для кулинарной книги")
app.include_router(router)
