"""API router for recipe-related endpoints and Kafka integration."""
import json
import math
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from urllib.parse import unquote
from app.database import pool
from app.repositories import recipe_repository
from app.services.recipe_service import search_pipeline
from app.producer.producer import send_recipes
from fastapi import HTTPException

router = APIRouter()


class Recipe(BaseModel):
    """Pydantic model defining the structure of a recipe."""
    title: str
    ingredients: list
    instructions: str


@router.post("/recipes")
async def create_recipe(recipe: Recipe):
    """Send a newly created recipe object to the Kafka topic."""
    send_recipes(recipe.model_dump())
    return {"status": "Recipe sent to Kafka", "data": recipe}


def clean_json(obj):
    """Recursively replace NaN and Infinity values with None for valid JSON."""
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_json(i) for i in obj]
    return obj


@router.get("/recipes/search")
async def search_recipes(
    query: str,
    number: int = Query(5, le=10),
    offset: int = 0
):
    """Search for recipes, filter results, send to Kafka, and return formatted response."""
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
    row = recipe_repository.get_by_title(unquote(title))
    if not row:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return {
        "title": row[0],
        "image": row[1],
        "cooking_minutes": row[2],
        "servings": row[3],
        "instructions": row[4],
        "ingredients_raw": json.loads(row[5]) if row[5] else [],
        "ingredients_normalized": json.loads(row[6]) if row[6] else [],
    }