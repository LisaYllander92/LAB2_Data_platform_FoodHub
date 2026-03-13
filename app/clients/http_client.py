import httpx
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class HttpClient:

    async def get(self, url: str, schema: Type[T], params: dict | None = None) -> T:

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

        response.raise_for_status()

        data = response.json()

        return schema.model_validate(data)