from fastapi import APIRouter, Query

from app.services.recipe_service import search_pipeline # hämtar det transformerade APIe:et
from app.producer.producer import send_recipes # connectar till producern

router = APIRouter()

# FastAPI-endpoint som tar emot användarens sökning
@router.get("/recipes/search")
async def search_recipes(
    query: str,
    number: int = Query(5, le=10),
    offset: int = 0
):
    result = await search_pipeline(query, number, offset) #Kör pipeline-koden
    send_recipes(query) # Skickar söktermen till Kafka-topicet.
    return result