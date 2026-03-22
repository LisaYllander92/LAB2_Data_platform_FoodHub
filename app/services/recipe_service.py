"""Recipe service pipeline for searching, fetching, transforming, and storing recipes.

Implements a cache-first strategy: checks curated_recipes before calling
the Spoonacular API to minimize token usage and API costs.
"""
import json
import pandas as pd
from app.clients.spoonacular_client import search_recipes, get_recipe_information
from app.transformers.recipe_transformers import transform_recipe
from app.services.ingredient_service import has_ingredient
from app.database import pool


def save_to_curated(recipe: dict):
    """Save a transformed recipe to the curated table, skipping duplicates."""
    try:
        with pool.connection() as conn:
            conn.execute("""
                INSERT INTO curated_recipes 
                    (title, image, cooking_minutes, servings, instructions, ingredients, ingredients_normalized)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (title) DO NOTHING
            """, (
                recipe.get("title"),
                recipe.get("image"),
                recipe.get("cooking_minutes") or recipe.get("ready_in_minutes"),
                recipe.get("servings"),
                recipe.get("instructions"),
                json.dumps(recipe.get("ingredients_raw", [])),
                json.dumps(recipe.get("ingredients_normalized", []))
            ))
    except Exception as e:
        print(f"Failed to save to curated_recipe: {e}")


async def search_pipeline(query: str, number: int, offset: int):
    """Execute the full recipe search pipeline using a cache-first strategy.

    Checks curated_recipes for matching titles before calling Spoonacular.
    If cached results are found, returns them directly without API cost.
    Otherwise fetches from Spoonacular, transforms, saves to curated, and returns.
    """
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT title,
                               image,
                               cooking_minutes,
                               servings,
                               instructions,
                               ingredients,
                               ingredients_normalized
                        FROM curated_recipes
                        WHERE ingredients_normalized::text ILIKE %s
                          AND ingredients_normalized IS NOT NULL
                            LIMIT %s
                        """, (f"%{query.lower()}%", number))
            cached = cur.fetchall()

    if cached:
        print(f"Cache hit for '{query}' — no API cost.")
        recipes = [
            {
                "title": r[0],
                "image": r[1],
                "cooking_minutes": r[2],
                "servings": r[3],
                "instructions": r[4],
                "ingredients_raw": (r[5]) if r[5] else [],
                "ingredients_normalized": (r[6]) if r[6] else [],
                "ingredients": (r[6]) if r[6] else []
            }
            for r in cached
        ]

        df = pd.DataFrame(recipes)
        if df.empty:
            return {"recipes": [], "totalResults": 0, "offset": offset, "number": number}

        if "ingredients_normalized" in df.columns:
            df["ingredients"] = df["ingredients_normalized"]

        matches = has_ingredient(query, df, save=False)
        return {
            "recipes": matches.to_dict(orient="records"),
            "totalResults": len(recipes),
            "offset": offset,
            "number": number
        }

    print(f"Cache miss for '{query}' — calling Spoonacular.")
    search_response = await search_recipes(query, number, offset)
    recipes = []

    for r in search_response.results:
        full_recipe = await get_recipe_information(r.id)
        recipe = transform_recipe(full_recipe)
        recipe_dict = recipe.model_dump()
        save_to_curated(recipe_dict)
        recipes.append(recipe_dict)

    df = pd.DataFrame(recipes)
    if df.empty:
        return {"recipes": [], "totalResults": 0, "offset": offset, "number": number}

    if "ingredients_normalized" in df.columns:
        df["ingredients"] = df["ingredients_normalized"]

    matches = has_ingredient(query, df, save=False)
    return {
        "recipes": matches.to_dict(orient="records"),
        "totalResults": search_response.totalResults,
        "offset": search_response.offset,
        "number": search_response.number
    }