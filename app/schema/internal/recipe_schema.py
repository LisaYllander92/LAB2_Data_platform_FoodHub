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
    image: Optional[str]

    servings: Optional[int]

    ready_in_minutes: Optional[int]
    cooking_minutes: Optional[int]
    preparation_minutes: Optional[int]

    instructions: Optional[str]

    ingredients: List[Ingredient]

    ingredients_raw: List[str]
    ingredients_normalized: List[str]

    dish_types: List[str]

    summary: Optional[str]
    source_url: Optional[str]