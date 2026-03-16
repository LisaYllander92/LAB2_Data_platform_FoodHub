from pydantic import BaseModel
from typing import List, Optional, Any

#Det här är er söksvarsmodell —
# den speglar vad Spoonacular returnerar när ni söker efter recept (till skillnad från recipe_information_schema som är detaljinfo om ett specifikt recept).

# Representerar ett enskilt recept i sökresultatet — bara grundinfo
# Används för att hämta ID:t och sedan anropa get_recipe_information()
class SpoonacularRecipeShort(BaseModel):
    id: int
    title: str
    image: Optional[str] = None
    imageType: Optional[str] = None

# Hela svaret från /recipes/complexSearch
class SpoonacularSearchResponse(BaseModel):
    offset: int
    number: int
    totalResults: int
    results: List[SpoonacularRecipeShort] = []
