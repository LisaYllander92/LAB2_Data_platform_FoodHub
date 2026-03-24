"""Recipe service pipeline for searching, fetching, transforming, and storing recipes.

Implements a cache-first strategy: checks curated_recipes before calling
the Spoonacular API to minimize token usage and API costs.
"""
import json
import pandas as pd
from rapidfuzz import fuzz
from app.clients.spoonacular_client import search_recipes, get_recipe_information
from app.repositories import recipe_repository
from app.transformers.recipe_transformers import transform_recipe
from app.services.ingredient_service import has_ingredient


def save_to_curated(recipe: dict):
    """Save a transformed recipe to the curated table, skipping duplicates."""
    try:
        recipe_repository.save_recipe(recipe)
    except Exception as e:
        print(f"Failed to save to curated_recipe: {e}")


async def search_pipeline(query: str, number: int, offset: int):
    """Execute the full recipe search pipeline using a cache-first strategy.

    Checks curated_recipes for matching ingredients before calling Spoonacular.
    If cached results are found, returns them directly without API cost.
    Otherwise fetches from Spoonacular, transforms, saves to curated, and returns.
    """
    search_terms = [s.strip() for s in query.replace(",", " ").split() if s.strip()]

    cached = recipe_repository.get_cached_by_terms(search_terms, number)

    if not cached:
        all_rows = recipe_repository.get_all_cached()
        cached = []
        for row in all_rows:
            ing_list = json.loads(row[6]) if row[6] else []
            # Fallback: fuzzy match against all cached rows if exact ILIKE query returned nothing
            any_terms_match = any(
                any(fuzz.partial_ratio(term, ing) >= 80 for ing in ing_list)
                for term in search_terms
            )
            if any_terms_match:
                cached.append(row)
        cached = cached[:number]

    if cached:
        print(f"Cache hit for '{query}' — no API cost.")
        recipes = [
            {
                "title": r[0],
                "image": r[1],
                "cooking_minutes": r[2],
                "servings": r[3],
                "instructions": r[4],
                "ingredients_raw": json.loads(r[5]) if r[5] else [],
                "ingredients_normalized": json.loads(r[6]) if r[6] else [],
                "ingredients": json.loads(r[6]) if r[6] else []
            }
            for r in cached
        ]

        df = pd.DataFrame(recipes)
        if df.empty:
            return {"recipes": [], "totalResults": 0, "offset": offset, "number": number}

        if "ingredients_normalized" in df.columns:
            df["ingredients"] = df["ingredients_normalized"]

        matches = has_ingredient(query, df)
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