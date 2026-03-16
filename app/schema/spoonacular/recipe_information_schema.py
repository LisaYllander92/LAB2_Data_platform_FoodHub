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
    measures: SpoonacularMeasures
    meta: List[str]


class SpoonacularRecipeInformation(BaseModel):

    id: int
    title: str
    image: str

    servings: Optional[int]
    readyInMinutes: Optional[int]
    cookingMinutes: Optional[int]
    preparationMinutes: Optional[int]

    sourceUrl: Optional[str]
    summary: Optional[str]
    instructions: Optional[str]

    dishTypes: List[str] = []

    extendedIngredients: List[SpoonacularIngredient]