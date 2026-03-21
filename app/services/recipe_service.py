import json
import pandas as pd
from app.clients.spoonacular_client import search_recipes, get_recipe_information
from app.transformers.recipe_transformers import transform_recipe
from app.services.ingredient_service import has_ingredient
from app.database import pool

def save_to_curated(recipe: dict):
    """
    Sparar ett recept i curated_recipes tabellen
    ON CONFLICT (title) DO NOTHING, hoppar över recept som redan finns
    """
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
                json.dumps(recipe.get("ingredients_raw", [])) # Spara som JSON-string
            ))
    except Exception as e:
        print(f"Failed to save to curated_recipe: {e}")

# Kollar curated_recipes innan det anropar Spoonacular API
# sök recept → hämta detaljer för varje recept → transformera → filtrera på ingrediens
async def search_pipeline(query: str, number: int, offset: int):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT title, image, cooking_minutes, servings, instructions, ingredients
                FROM curated_recipes
                WHERE LOWER(title) LIKE %s
                LIMIT %s
            """, (f"%{query.lower()}%", number))
            # hämtar alla matchande rader som tuples
            cached = cur.fetchall()

    if cached:
        # vi hittade recept i databasen - ingen API kostnad!
        print(f"Cachesökning för '{query}' ingen kostnad")

        # samma format som spoonacular
        # Gör varje tuple till ett dict
        recipes =[
            {
                "title": r[0],
                "image": r[1],
                "cooking_minutes": r[2],
                "servings": r[3],
                "instructions": r[4],
                # Konverterar från JSON-string till lista 
                "ingredients_raw": json.loads(r[5]) if r[5] else [],
                # Används av has_ingridient() för fuzzy search
                "ingredients": json.loads(r[5]) if r[5] else []
            }
            for r in cached
        ]
        
        
        df = pd.DataFrame(recipes)
        
        # Kör fuzzy search 
        matches = has_ingredient(query, df, save=False)

        return {
            "recipes": matches.to_dict(orient="records"),
            "totalResults": len(recipes),
            "offset": offset,
            "number": number
        }
    # Fanns inte i curated, anropar spoonacular
    print(f"Ingen resultat för cachesökning '{query}' anropar spoonacular...")
    search_response = await search_recipes(query, number, offset)

    recipes = []
    for r in search_response.results:
        # hämtar receptinfo från spoonacular med ReceptId
        full_recipe = await get_recipe_information(r.id)

        # Omvandlar spoonacular format till vårat recipe-schema
        recipe = transform_recipe(full_recipe)

        # Konverterar pydantic till dict
        recipe_dict = recipe.model_dump()

        # sparar i curated_recipes
        save_to_curated(recipe_dict)

        recipes.append(recipe_dict)

    df = pd.DataFrame(recipes)
    matches = has_ingredient(query, df, save=False)

    return {
        "recipes": matches.to_dict(orient="records"),
        "totalResults": search_response.totalResults,
        "offset": search_response.offset,
        "number": search_response.number
    }