from pydantic import BaseModel
from typing import List, Optional, Any


class SpoonacularRecipeShort(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    imageType: Optional[str] = None


class SpoonacularSearchResponse(BaseModel):
    offset: int
    number: int
    totalResults: int
    results: List[SpoonacularRecipeShort] = []