from pydantic import BaseModel


class RecipeBase(BaseModel):
    title: str
    cook_time: int
    ingredients: str
    description: str


class RecipeCreate(RecipeBase):
    pass


class RecipeOut(RecipeBase):
    id: int
    views: int
