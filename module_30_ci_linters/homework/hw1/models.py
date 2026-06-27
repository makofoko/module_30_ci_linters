from sqlalchemy import Column, Integer, String, Text

from module_30_ci_linters.homework.hw1.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    cook_time = Column(Integer, nullable=False)
    ingredients = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    views = Column(Integer, default=0)