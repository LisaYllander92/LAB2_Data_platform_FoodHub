import httpx # Asynkront HTTP-bibliotek, används istället för requests när man kör async kod.
# TypeVar och Type används för att göra klassen generisk —
# den kan returnera olika Pydantic-modeller beroende på vad man skickar in.
from typing import Type, TypeVar
from pydantic import BaseModel

# Skapar en platshållare för "vilken Pydantic-modell som helst".
# bound=BaseModel betyder att T måste vara en Pydantic-modell.
T = TypeVar("T", bound=BaseModel)

# En klass med en asynkron get-metod. Tar emot:
# url — vart man ska anropa
# schema — vilken Pydantic-modell svaret ska valideras mot
# params — valfria query-parametrar (t.ex. ?query=avocado)
class HttpClient:


    ## usage example, modular get. interface - await http_client.get(url, Response, params)
    async def get(self, url: str, schema: Type[T], params: dict | None = None) -> T:
        # Öppnar en HTTP-session, gör anropet och stänger sessionen automatiskt efteråt.
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

        # Kastar ett fel om APIet svarar med t.ex. 404 eller 500 — bra felhantering för VG.
        response.raise_for_status()
        # Parsar JSON-svaret och validerar det mot Pydantic-modellen. Om APIet returnerar fel data kastar Pydantic ett fel.
        data = response.json()
        return schema.model_validate(data)

#Användare söker "avocado"
#         ↓
# FastAPI endpoint (/recipes/search)
#         ↓
# HttpClient anropar Spoonacular
#         ↓
# Spoonacular svarar med rå JSON
#         ↓
# HttpClient validerar JSON → Pydantic-modell
#         ↓
# transform_recipe() omvandlar till ert format
#         ↓
# sparas i databasen / skickas tillbaka till användaren


