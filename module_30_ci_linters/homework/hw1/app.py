from fastapi import FastAPI
from routes import router
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cookbook API", description="API для кулинарной книги")

app.include_router(router)
