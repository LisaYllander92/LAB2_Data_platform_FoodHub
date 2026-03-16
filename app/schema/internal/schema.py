from pydantic import BaseModel, field_validator
from typing import Optional, List, Any

#Det här är er interna modell för lokal JSON-data —
# används för att validera recepten från cleaning_recipe.json (er lokala datakälla), inte från Spoonacular.

# Representerar ett recept från den lokala JSON-filen (cleaning_recipe.json)
# Används i flagged_recipe.py för att validera lokal data
class FoodData(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    cooking_minutes: Optional[int] = None
    ingredients: List[str] = []
    servings: Optional[int] = None
    instructions: Optional[str] = None
    allergies: Optional[List[str]] = None

    # Körs innan vanlig validering på cooking_minutes och servings
    # Om värdet är None eller tom sträng returneras 0 istället för att krascha
    @field_validator("cooking_minutes", "servings", mode="before")
    @classmethod
    def replace_empty_with_zero(cls, v: Any) -> int:
        if v is None or v == "":
            return 0
        return v
