from pydantic import BaseModel, field_validator
from typing import Optional, List, Any


class FoodData(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    cooking_minutes: Optional[int] = None
    ingredients: List[str] = []
    servings: Optional[int] = None
    instructions: Optional[str] = None
    allergies: Optional[List[str]] = None

    @field_validator("cooking_minutes", "servings", mode="before")
    @classmethod
    def replace_empty_with_zero(cls, v: Any) -> int:
        if v is None or v == "":
            return 0
        return v
