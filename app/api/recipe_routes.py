"""API router for recipe-related endpoints and Kafka integration."""
import json
import math
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from urllib.parse import unquote
from app.repositories import recipe_repository
from app.repositories.recipe_repository import log_search_query
from app.services.recipe_service import search_pipeline
from app.producer.producer import send_recipes
from app.services.statistics_service import plot_popular_searches

router = APIRouter()


class Recipe(BaseModel):
    """Request body model for manually creating a recipe via POST."""
    title: str
    ingredients: list
    instructions: str


def clean_json(obj):
    """Recursively replace NaN and Infinity float values with None for JSON compatibility."""
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_json(i) for i in obj]
    return obj

@router.post("/recipes")
async def create_recipe(recipe: Recipe):
    """Accept a recipe payload and forward it to Kafka."""
    send_recipes(recipe.model_dump())
    return {"status": "Recipe sent to Kafka", "data": recipe}


@router.get("/recipes/search")
async def search_recipes(
    query: str,
    number: int = Query(5, le=10),
    offset: int = 0
):
    """Search for recipes matching the query using the cache-first pipeline."""
    log_search_query(query)
    result = await search_pipeline(query, number, offset)

    if result["recipes"]:
        send_recipes(result["recipes"])

    formatted_recipes = [
        {
            "title": r["title"],
            "servings": r["servings"],
            "ingredients": r["ingredients_raw"],
            "instructions": r["instructions"]
        }
        for r in result["recipes"]
    ]

    return JSONResponse(content=clean_json({
        "recipes": formatted_recipes,
        "totalResults": result["totalResults"],
        "offset": result["offset"],
        "number": result["number"]
    }))


@router.get("/recipes/history")
def get_recipe_history(limit: int = Query(20, le=100)):
    """Return the most recently added recipes from the curated table."""
    rows = recipe_repository.get_history(limit)
    return [
        {
            "id": row[0],
            "title": row[1],
            "image": row[2],
            "cooking_minutes": row[3],
            "servings": row[4],
            "created_at": row[5].isoformat() if row[5] else None,
        }
        for row in rows
    ]


@router.get("/recipes/detail/{title}")
def get_recipe_detail(title: str):
    """Return full details for a single recipe by title and mark it as viewed."""
    decoded = unquote(title)
    row = recipe_repository.get_by_title(decoded)
    if not row:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe_repository.mark_viewed(decoded)
    return {
        "title": row[0],
        "image": row[1],
        "cooking_minutes": row[2],
        "servings": row[3],
        "instructions": row[4],
        "ingredients_raw": json.loads(row[5]) if row[5] else [],
        "ingredients_normalized": json.loads(row[6]) if row[6] else [],
    }


@router.get("/recipes/popular-searches")
def get_popular_searches():
    """Return the top 10 most searched ingredient terms."""
    return recipe_repository.get_popular_searches()


@router.get("/recipes/stats/plot")
def get_search_plot():
    """Generate and return a bar chart of popular searches as a PNG image."""
    img = plot_popular_searches()
    if not img:
        raise HTTPException(status_code=404, detail="No data to display")
    return Response(content=img, media_type="image/png")


@router.get("/recipes/stats")
def get_stats():
    """Return aggregated search and recipe statistics and forward the event to Kafka."""
    data = recipe_repository.get_stats()
    send_recipes({"event": "stats_viewed", "data": data})
    return data