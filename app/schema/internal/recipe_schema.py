from pydantic import BaseModel
from typing import List, Optional


class Ingredient(BaseModel):
    id: int
    name: str
    original: str
    amount: float
    unit: str


class Recipe(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    servings: Optional[int] = None
    ready_in_minutes: Optional[int] = None
    cooking_minutes: Optional[int] = None
    preparation_minutes: Optional[int] = None
    instructions: Optional[str] = None
    ingredients: List[Ingredient] = []
    ingredients_raw: List[str] = []
    ingredients_normalized: List[str] = []
    dish_types: List[str] = []
    summary: Optional[str] = None
    source_url: Optional[str] = None