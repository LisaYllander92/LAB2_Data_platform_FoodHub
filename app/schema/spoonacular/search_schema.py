from pydantic import BaseModel
from typing import List

#Det här är er söksvarsmodell —
# den speglar vad Spoonacular returnerar när ni söker efter recept (till skillnad från recipe_information_schema som är detaljinfo om ett specifikt recept).

# Representerar ett enskilt recept i sökresultatet — bara grundinfo
# Används för att hämta ID:t och sedan anropa get_recipe_information()
class SpoonacularRecipeShort(BaseModel):
    id: int
    title: str
    image: str
    imageType: str

# Hela svaret från /recipes/complexSearch
class SpoonacularSearchResponse(BaseModel):
    offset: int         # var i resultatlistan vi börjar, används för paginering
    number: int         # antal recept som returnerades
    totalResults: int   # totalt antal träffar i Spoonacular
    results: List[SpoonacularRecipeShort]  # lista med korta receptobjekt


    #**Kopplingen till projektet:**
# ```
# search_recipes()
#         ↓
# Spoonacular svarar med lista av korta recept
#         ↓
# SpoonacularSearchResponse validerar svaret
#         ↓
# for r in search_response.results:
#     get_recipe_information(r.id)  ← hämtar fullständig info per recept