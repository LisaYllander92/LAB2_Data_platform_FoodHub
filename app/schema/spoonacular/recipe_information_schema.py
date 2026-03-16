from pydantic import BaseModel
from typing import List, Optional


class SpoonacularMeasure(BaseModel):
    amount: float
    unitLong: str
    unitShort: str


class SpoonacularMeasures(BaseModel):
    metric: SpoonacularMeasure
    us: SpoonacularMeasure


class SpoonacularIngredient(BaseModel):
    id: int
    name: str
    original: str
    amount: float
    unit: str
    measures: Optional[SpoonacularMeasures] = None
    meta: List[str] = []


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