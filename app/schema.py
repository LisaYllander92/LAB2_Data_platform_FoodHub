from pydantic import BaseModel
from typing import Optional, List

class FoodData(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    cooking_minutes: Optional[int] = None
    ingredients: List[str]
    servings: Optional[int] = None
    instructions: Optional[str] = None
    allergies: Optional[List[str]] = None


