import math
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.recipe_service import search_pipeline
from app.producer.producer import send_recipes

router = APIRouter()

# Definiera hur ett recept ska se ut (Schema)
class Recipe(BaseModel):
    title: str
    ingredients: list
    instructions: str

@router.post("/recipes")
async def create_recipe(recipe: Recipe):
    # Här skickar vi hela recept-objektet till Kafka
    send_recipes(recipe.dict())
    return {"status": "Recipe sent to Kafka", "data": recipe}


def clean_json(obj):
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
    result = await search_pipeline(query, number, offset)
    send_recipes(query)
    return JSONResponse(content=clean_json(result))