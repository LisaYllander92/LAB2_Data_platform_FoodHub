# Det här är er Spoonacular-klient — den enda filen som pratar direkt med Spoonaculars API.

import os
from app.clients.http_client import HttpClient
from app.schema.spoonacular.search_schema import SpoonacularSearchResponse
from app.schema.spoonacular.recipe_information_schema import SpoonacularRecipeInformation

# Sätter upp bas-URL, hämtar API-nyckeln från .env och skapar en instans av HttpClient.
BASE_URL = "https://api.spoonacular.com"
API_KEY = os.getenv("SPOONACULAR_API_KEY")

http_client = HttpClient()

# search_recipes() -  Söker recept och returnerar ett SpoonacularSearchResponse-objekt.
async def search_recipes(query: str, number: int, offset: int):
    url = f"{BASE_URL}/recipes/complexSearch"
    params = {
        "query": query,
        "number": number,
        "offset": offset,
        "apiKey": API_KEY
    }

    return await http_client.get(url, SpoonacularSearchResponse, params)

# get_recipe_information() -
async def get_recipe_information(recipe_id: int):
    url = f"{BASE_URL}/recipes/{recipe_id}/information"
    params = {
        "includeNutrition": False,
        "apiKey": API_KEY
    }
    # Hämtar fullständig info om ett specifikt recept via dess ID.
    return await http_client.get(url, SpoonacularRecipeInformation, params)

# Dessa två funktioner används sedan i search_pipeline() som vi gick igenom tidigare.
# Bra separation — all Spoonacular-logik ligger samlat här.