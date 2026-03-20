"""Pydantic schemas mirroring the Spoonacular API search response.

This module handles the initial search results from the /recipes/complexSearch 
endpoint, which returns basic recipe information (unlike the detailed info).

Project Flow:
    1. search_recipes() is called.
    2. Spoonacular returns a list of short recipes.
    3. SpoonacularSearchResponse validates the response.
    4. For each result, get_recipe_information(result.id) is called 
       to fetch full details.
"""
from pydantic import BaseModel
from typing import List, Optional


class SpoonacularRecipeShort(BaseModel):
    """Model representing a single recipe in the search results with basic info.

    Used primarily to extract the recipe ID in order to fetch detailed 
    information via get_recipe_information().
    """
    id: int
    title: str
    image: Optional[str] = None
    imageType: Optional[str] = None


class SpoonacularSearchResponse(BaseModel):
    """Model representing the full response from the /recipes/complexSearch endpoint.

    Attributes:
        offset (int): Starting position in the result list, used for pagination.
        number (int): The number of recipes returned.
        totalResults (int): The total number of matching recipes in Spoonacular.
        results (List[SpoonacularRecipeShort]): A list of short recipe objects.
    """
    offset: int
    number: int
    totalResults: int
    results: List[SpoonacularRecipeShort] = []