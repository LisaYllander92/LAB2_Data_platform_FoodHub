import pandas as pd
from app.clients.spoonacular_client import (
    search_recipes,
    get_recipe_information
)
from app.transformers.recipe_transformers import transform_recipe

from app.services.ingredient_service import has_ingredient


async def search_pipeline(query: str, number: int, offset: int):

    search_response = await search_recipes(query, number, offset)
    recipes = []
    for r in search_response.results:
        full_recipe = await get_recipe_information(r.id)
        recipe = transform_recipe(full_recipe)
        recipes.append(recipe.model_dump())

    df = pd.DataFrame(recipes)
    matches = has_ingredient(query, df)

    return {
        "recipes": matches.to_dict(orient="records"),
        "totalResults": search_response.totalResults,
        "offset": search_response.offset,
        "number": search_response.number
    }