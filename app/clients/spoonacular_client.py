"""Spoonacular API client for searching and retrieving recipe details."""
import os
from app.clients.http_client import HttpClient
from app.schema.spoonacular.search_schema import SpoonacularSearchResponse
from app.schema.spoonacular.recipe_information_schema import SpoonacularRecipeInformation

BASE_URL = "https://api.spoonacular.com"
API_KEY = os.getenv("SPOONACULAR_API_KEY")

http_client = HttpClient()


async def search_recipes(query: str, number: int, offset: int) -> SpoonacularSearchResponse:
    """Search for recipes matching the query and return a list of short recipe results."""
    url = f"{BASE_URL}/recipes/complexSearch"
    params = {
        "query": query,
        "number": number,
        "offset": offset,
        "apiKey": API_KEY
    }
    return await http_client.get(url, SpoonacularSearchResponse, params)


async def get_recipe_information(recipe_id: int) -> SpoonacularRecipeInformation:
    """Fetch full recipe details for a given recipe ID."""
    url = f"{BASE_URL}/recipes/{recipe_id}/information"
    params = {
        "includeNutrition": False,
        "apiKey": API_KEY
    }
    return await http_client.get(url, SpoonacularRecipeInformation, params)