from pydantic import BaseModel
from typing import List


class SpoonacularRecipeShort(BaseModel):
    id: int
    title: str
    image: str
    imageType: str


class SpoonacularSearchResponse(BaseModel):
    offset: int
    number: int
    totalResults: int
    results: List[SpoonacularRecipeShort]