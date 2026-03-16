from fastapi import APIRouter, Query

from app.services.recipe_service import search_pipeline
from app.producer.producer import send_recipes

router = APIRouter()


@router.get("/recipes/search")
async def search_recipes(
    query: str,
    number: int = Query(5, le=10),
    offset: int = 0
):
    result = await search_pipeline(query, number, offset)
    send_recipes(query)
    return result