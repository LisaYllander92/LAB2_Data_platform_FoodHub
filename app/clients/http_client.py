"""HTTP client utility for making asynchronous requests and validating responses."""
import httpx
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class HttpClient:
    """Generic async HTTP client for fetching and validating API responses using Pydantic."""

    async def get(self, url: str, schema: Type[T], params: dict | None = None) -> T:
        """Send a GET request and validate the JSON response against the provided schema."""
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)

        response.raise_for_status()
        data = response.json()
        return schema.model_validate(data)