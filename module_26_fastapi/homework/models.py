from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cook_time = Column(Integer)
    views = Column(Integer, default=0)
    ingredients = Column(Text)
    description = Column(Text)
