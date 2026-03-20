"""Pydantic schemas mirroring the exact Spoonacular API response for specific recipes."""
from pydantic import BaseModel, field_validator
from typing import List, Optional, Any
import math


def clean_numeric(v: Any) -> Any:
    """Clean numeric values by converting empty strings, NaN, and Inf to None."""
    if v is None or v == "":
        return None
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
        return None
    return v


class SpoonacularMeasure(BaseModel):
    """Model representing a specific measurement unit (e.g., '2.5 cups' or '590 milliliters')."""
    amount: float
    unitLong: str
    unitShort: str


class SpoonacularMeasures(BaseModel):
    """Container for both metric and US measurements of an ingredient."""
    metric: SpoonacularMeasure
    us: SpoonacularMeasure


class SpoonacularIngredient(BaseModel):
    """Model representing a single ingredient returned by the Spoonacular API."""
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
        """Validate and clean the amount field, defaulting to 0.0 if invalid."""
        return clean_numeric(v) or 0.0


class SpoonacularRecipeInformation(BaseModel):
    """Full recipe response model from the Spoonacular API used in get_recipe_information()."""
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
        """Clean numeric fields to handle empty strings, NaN, or Inf before standard validation."""
        return clean_numeric(v)