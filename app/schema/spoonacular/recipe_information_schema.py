from pydantic import BaseModel, field_validator
from typing import List, Optional, Any
import math

def clean_numeric(v: Any) -> Any:
    if v is None or v == "":
        return None
    #om värdet är ett flyttal OCH är antingen NaN (Not a Number) eller Inf (oändlighet), returnera None
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v

#Det här är er Spoonacular-svarsmodell —
# den speglar exakt hur Spoonaculars API svarar när ni hämtar ett specifikt recept.

# Representerar en måttenhet, t.ex. "2.5 cups" eller "590 milliliters"
class SpoonacularMeasure(BaseModel):
    amount: float
    unitLong: str
    unitShort: str

# Innehåller både metriska och amerikanska mått för en ingrediens
class SpoonacularMeasures(BaseModel):
    metric: SpoonacularMeasure
    us: SpoonacularMeasure

# Representerar en enskild ingrediens som Spoonacular returnerar
class SpoonacularIngredient(BaseModel):
    id: int
    name: str
    original: str
    amount: float
    unit: str
    measures: Optional[SpoonacularMeasures] = None
    meta: List[str] = []

    @field_validator("amount", mode="before")
    @classmethod
    def validate_numeric(cls, v):
        return clean_numeric(v) or 0.0

# Hela receptsvaret från Spoonacular — används i get_recipe_information()
class SpoonacularRecipeInformation(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    servings: Optional[int] = None
    readyInMinutes: Optional[int] = None
    cookingMinutes: Optional[int] = None
    preparationMinutes: Optional[int] = None
    sourceUrl: Optional[str] = None
    summary: Optional[str] = None
    instructions: Optional[str] = None
    dishTypes: List[str] = []
    extendedIngredients: List[SpoonacularIngredient] = []

    @field_validator("servings", "readyInMinutes", "cookingMinutes", "preparationMinutes", mode="before")
    @classmethod
    def validate_numeric(cls, v):
        return clean_numeric(v)
