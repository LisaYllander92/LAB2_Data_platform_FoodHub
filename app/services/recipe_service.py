import json
import pandas as pd
from app.clients.spoonacular_client import search_recipes, get_recipe_information
from app.transformers.recipe_transformers import transform_recipe
from app.services.ingredient_service import has_ingredient
from app.database import pool

def save_to_curated(recipe: dict):
    try:
        with pool.connection() as conn:
            conn.execute("""
                INSERT INTO curated_recipes 
                    (title, image, cooking_minutes, servings, instructions, ingredients)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (title) DO NOTHING
            """, (
                recipe.get("title"),
                recipe.get("image"),
                recipe.get("cooking_minutes") or recipe.get("ready_in_minutes"),
                recipe.get("servings"),
                recipe.get("instructions"),
                json.dumps(recipe.get("ingredients_raw", []))
            ))
    except Exception as e:
        print(f"Failed to save to curated_recipe: {e}")

# sök recept → hämta detaljer för varje recept → transformera → filtrera på ingrediens
async def search_pipeline(query: str, number: int, offset: int):
    search_response = await search_recipes(query, number, offset)
    recipes = []
    for r in search_response.results:
        full_recipe = await get_recipe_information(r.id)
        recipe = transform_recipe(full_recipe)
        recipe_dict = recipe.model_dump() # ändrad!

        save_to_curated(recipe_dict)  # ändrad ← sparar till curated_recipe
        recipes.append(recipe_dict)

    df = pd.DataFrame(recipes)
    matches = has_ingredient(query, df)

    return {
        "recipes": matches.to_dict(orient="records"),
        "totalResults": search_response.totalResults,
        "offset": search_response.offset,
        "number": search_response.number
    }